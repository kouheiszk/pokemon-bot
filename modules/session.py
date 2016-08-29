#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import time

from modules.api import Api
from modules.exceptions import GeneralPokemonBotException
from modules.item import Item
from modules.location import Location
from modules.pokedex import Pokedex
from modules.route import Route
from modules.state import State

log = logging.getLogger("pokemon_bot")


class Session(object):
    def __init__(self, auth_service, username, password, location_lookup=None):
        self._location = Location(location_lookup)
        self._api = Api(auth_service, username, password, self.location)
        self._state = State()

    def __getattr__(self, item):
        return getattr(self._state, item)

    @property
    def location(self):
        return self._location

    def get_profile(self, delay=5):
        log.info(">> プロフィール取得...")
        self._api.get_player(self._state, delay=delay)
        return self._state.player

    def get_map_objects(self, radius=10, both_direction=True, delay=10):
        cell_ids = self.location.get_cell_ids(radius=radius, both_direction=both_direction)
        self._api.get_map_objects(self._state, cell_ids=cell_ids, delay=delay)
        return self._state.map_objects

    def clean_pokemon(self, threshold_rate=20, delay=5):
        log.info(">> 博士にポケモンを送る...")

        evolvable_pokemon_ids = [Pokedex.PIDGEY.value, Pokedex.RATTATA.value, Pokedex.ZUBAT.value]
        to_evolve_pokemons = {pokemon_id: [] for pokemon_id in evolvable_pokemon_ids}

        # 進化コストのかからないポケモン以外を博士に返す
        for _, pokemon in self._state.inventory.party.items():
            # 規定のCP以下のポケモンは博士に返す
            if pokemon.cp < pokemon.max_cp * threshold_rate / 100:
                if pokemon.pokemon_id in evolvable_pokemon_ids:
                    to_evolve_pokemons[pokemon.pokemon_id].append(pokemon)
                    continue

                log.info("> {}を送る (CP:{} < {}x{}%)...".format(pokemon.name, pokemon.cp, pokemon.max_cp, threshold_rate))
                self._api.release_pokemon(pokemon, delay=delay)

        # ポケモンを進化させる
        for pokemon_id in evolvable_pokemon_ids:
            if pokemon_id not in self._state.inventory.candies:
                # キャンディーが無いということはポケモンを捕まえていないということ
                continue

            candies = self._state.inventory.candies[pokemon_id]
            pokemons = to_evolve_pokemons[pokemon_id]
            # キャンディーの分進化させ、進化後のポケモンを博士に送る
            while candies // Pokedex(pokemon_id).evolve_candies < len(pokemons):
                pokemon = pokemons.pop()
                log.info("> {}を送る...".format(pokemon.name))
                self._api.release_pokemon(pokemon, delay=delay)
                candies += 1

            # アメが足りなく進化できなかったポケモンを博士に送る
            for pokemon in pokemons:
                log.info("> {}を進化...".format(pokemon.name))
                evolve_result = self._api.evolve_pokemon(self._state, pokemon, delay=delay)
                log.info(evolve_result)
                log.info("> {}を送る...".format(pokemon.name))
                self._api.release_pokemon(pokemon, delay=delay)

    def clean_inventory(self, delay=5):
        log.info(">> アイテムポーチの中身を整理...")
        bag = self._state.inventory.bag

        # Clear out all of a crtain type
        tossable_item_ids = [Item.POTION.value, Item.SUPER_POTION.value, Item.REVIVE.value]
        for item_id in tossable_item_ids:
            if item_id in bag and bag[item_id] > 0:
                self._api.recycle_inventory_item(self._state, item_id,
                                                 count=bag[item_id],
                                                 delay=delay)

        # Limit a certain type
        limited_items = {
            Item.POKE_BALL.value: 50,
            Item.GREAT_BALL.value: 100,
            Item.ULTRA_BALL.value: 150,
            Item.RAZZ_BERRY.value: 25
        }
        for item_id in limited_items:
            if item_id in bag and bag[item_id] > limited_items[item_id]:
                log.debug("> {}を捨てる...".format(Item(item_id)))
                self._api.recycle_inventory_item(self._state, item_id,
                                                 count=(bag[item_id] - limited_items[item_id]),
                                                 delay=delay)

    def walk_and_catch(self, route, delay=10, catch_on_way=True):
        pokemon = route.instance
        # 歩き出す前にポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(pokemon):
            return None

        log.info(">> {}捕獲開始...".format(pokemon.name))
        self.walk_on(route, catch_on_way=catch_on_way)
        result = self.encounter_and_catch(pokemon)
        log.info(result)
        # ポケモンを捕まえた後はしばらく休む
        time.sleep(delay)

    def encounter_and_catch(self, pokemon, threshold_p=0.5, limit=10, delay=2):
        # ポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(pokemon):
            return None

        self._state.catch.start_catching(pokemon)

        # エンカウント開始
        encounter = self._api.encounter_pokemon(self._state, pokemon, delay=delay)

        # パーティーがいっぱいの場合
        if encounter.status.is_party_full:
            raise GeneralPokemonBotException("Can't catch! Party is full!")

        # それ以外の場合で捕まえられない場合はNoneを返す
        if not encounter.status.is_catchable:
            return None

        # Grab needed data from proto
        chances = encounter.capture_probability.get("capture_probability", [])
        balls = encounter.capture_probability.get("pokeball_type", [])
        balls = balls or [Item.POKE_BALL, Item.GREAT_BALL, Item.ULTRA_BALL]
        bag = self._state.inventory.bag

        # Attempt catch
        while True:
            best_ball = Item.UNKNOWN
            alt_ball = Item.UNKNOWN

            # Check for balls and see if we pass
            # wanted threshold
            for i, ball in enumerate(balls):
                if bag.get(ball, 0) > 0:
                    alt_ball = ball
                    if chances[i] > threshold_p:
                        best_ball = ball
                        break

            # If we can't determine a ball, try a berry
            # or use a lower class ball
            if best_ball == Item.UNKNOWN:
                if not encounter.berried and bag.get(Item.RAZZ_BERRY, 0) > 0:
                    log.info("> ラズベリーを使用...")
                    self._api.use_item_capture(Item.RAZZ_BERRY, pokemon, delay=delay + random.randint(0, 2))
                    encounter.berried = True
                    continue

                # if no alt ball, there are no balls
                elif alt_ball == Item.UNKNOWN:
                    raise GeneralPokemonBotException("Out of usable balls")
                else:
                    best_ball = alt_ball

            # ボールを投げる
            log.info("> {}を投げた...".format(Item(best_ball)))
            catch_pokemon_dict = self._api.catch_pokemon(self._state, pokemon, best_ball,
                                                         delay=delay + random.randint(0, 2))
            encounter.set_catch_pokemon_dict(catch_pokemon_dict)

            # Success or run away
            if encounter.attempt.status.is_success or encounter.attempt.status.is_flee:
                return encounter

            # Only try up to x attempts
            encounter.attempt_count += 1
            if encounter.attempt_count > limit:
                log.info("<< 試行上限をオーバー")
                return None

    # Walk to fort and spin
    def walk_and_spin(self, route):
        self.walk_on(route)
        self.spin_pokestop(route.instance)

    def spin_pokestop(self, pokestop, delay=2):
        details = self._api.get_fort_details(self._state, pokestop, delay=delay)
        fort_search_dict = self._api.get_fort_search(self._state, pokestop, delay=delay)
        details.set_fort_search_dict(fort_search_dict)
        log.info(">> ポケストップをスピン...")
        log.info("{}".format(details))

    def set_eggs(self):
        incubators = self._state.inventory.unused_incubators
        eggs = sorted(
            filter(lambda e: not e.egg_incubator_id, self._state.inventory.eggs.values()),
            key=lambda e: e.egg_km_walked_target - e.egg_km_walked_start,
            reverse=True)

        # 空の孵化器に距離の長い卵から入れる
        for i in range(min(len(incubators), len(eggs))):
            incubator = incubators[i]
            egg = eggs[i]
            log.info("Adding egg '{}' to '{}'.".format(egg.id, self._state.inventory.incubators[incubator.id]))
            self._api.use_item_egg_incubator(self._state, incubator, egg)

    def get_level_up_rewards(self):
        if self._state.inventory.stats.should_get_level_up_rewarded:
            rewards = self._api.level_up_rewards(self._state)
            log.info(">> レベルアップ...")
            log.info("{}".format(rewards))

    def set_coordinates(self, latitude, longitude, catch_on_way=True):
        self.location.set_position(latitude, longitude)
        self._api.set_coordinates(self.location.position)
        map_objects = self.get_map_objects(radius=1, delay=1)

        # 移動途中に在るスピン可能範囲内のポケストップは回す
        for pokestop in map_objects.get_spinable_pokestops(self.location.latitude, self.location.longitude):
            self.spin_pokestop(pokestop, delay=5)

        if catch_on_way and (map_objects.wild_pokemons or map_objects.catchable_pokemons):
            log.info(">> マップを取得...")
            log.info(map_objects)
            # 移動途中の捕まえられるポケモンは捕まえる
            for pokemon in (map_objects.wild_pokemons + map_objects.catchable_pokemons):
                self.walk_and_catch(Route(pokemon), catch_on_way=False)

    def walk_on(self, route, epsilon=10, step=2.4, catch_on_way=True):
        if route.legs is None:
            self.walk_to(route.instance.latitude,
                         route.instance.longitude,
                         epsilon=epsilon,
                         step=step,
                         catch_on_way=catch_on_way)
        else:
            for s in route.legs["steps"]:
                self.walk_to(s["end_location"]["lat"],
                             s["end_location"]["lng"],
                             epsilon=epsilon,
                             step=step,
                             catch_on_way=catch_on_way)

    def walk_to(self, olatitude, olongitude, epsilon=10, step=3.2, delay=10, catch_on_way=True):
        if step >= epsilon:
            raise GeneralPokemonBotException("Walk may never converge")

        # Calculate distance to position
        latitude, longitude, _ = self.location.get_position()
        dist = closest = Location.get_distance(latitude, longitude, olatitude, olongitude)

        # Run walk
        divisions = closest / step
        d_lat = (latitude - olatitude) / divisions
        d_lon = (longitude - olongitude) / divisions

        log.info("{}までの距離{:.2f}m. 徒歩{:.1f}秒. 現在位置: {}..."
                 .format("ポケストップ" if catch_on_way else "ポケモン", dist, dist / step, self.location))

        steps = 1
        while dist > epsilon:
            log.debug("歩いた距離 {0:.2f}m / {1:.2f}m".format(closest - dist, closest))
            latitude -= d_lat
            longitude -= d_lon
            steps %= delay
            if steps == 0:
                self.set_coordinates(latitude, longitude, catch_on_way=catch_on_way)
                if catch_on_way:
                    self.walk_to(olatitude, olongitude, epsilon=epsilon, step=step)
                    break
            else:
                time.sleep(1)
            dist = Location.get_distance(latitude, longitude, olatitude, olongitude)
            steps += 1

        # Finalize walk
        steps -= 1
        if steps % delay > 0 and not catch_on_way:
            delta = delay - steps
            time.sleep(delta)
            self.set_coordinates(latitude, longitude, catch_on_way=False)
