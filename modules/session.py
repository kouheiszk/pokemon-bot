#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import time

from IPython import embed

from modules.api import Api
from modules.exceptions import GeneralPokemonBotException
from modules.item import items
from modules.location import Location
from modules.pokedex import pokedex
from modules.state import State

log = logging.getLogger("pokemon_bot")


class Session(object):
    def __init__(self, location_lookup=None):
        self._location = Location(location_lookup)
        self._api = Api(self.location)
        self._state = State()

    def __getattr__(self, item):
        return getattr(self._state, item)

    @property
    def location(self):
        return self._location

    def authenticate(self, auth_service, username, password):
        log.info("Authenticate with {}...".format(auth_service))
        self._api.authenticate(auth_service, username, password)
        log.info("Authenticate success!!")

    def get_profile(self, delay=3):
        self._api.get_player(self._state, delay=delay)
        return self._state.player

    def get_inventory(self, delay=10):
        self._api.get_inventory(self._state, delay=delay)
        return self._state.inventory

    def get_map_objects(self, radius=10, both_direction=True, delay=10):
        log.info("Get Map Objects...")
        cell_ids = self.location.get_cell_ids(radius=radius, both_direction=both_direction)
        self._api.get_map_objects(self._state, cell_ids=cell_ids, delay=delay)
        return self._state.map_objects

    def clean_pokemon(self, threshold_cp=50, delay=5):
        log.info("Cleaning out Pokemon...")

        evolvable_pokemon_ids = [pokedex.PIDGEY, pokedex.RATTATA, pokedex.ZUBAT]
        to_evolve_pokemons = {pokemon_id: [] for pokemon_id in evolvable_pokemon_ids}

        # 進化コストのかからないポケモン以外を博士に返す
        for pokemon in self._state.inventory.party:
            # 規定のCP以下のポケモンは博士に返す
            if pokemon.cp < threshold_cp:
                if pokemon.id in evolvable_pokemon_ids:
                    to_evolve_pokemons[pokemon.pokemon_id].append(pokemon)
                    continue

                # Get rid of low CP, low evolve value
                log.info("Releasing {}...".format(pokedex[pokemon.pokemon_id]))
                self._api.release_pokemon(pokemon, delay=delay)

        # ポケモンを進化させる
        for pokemon_id in evolvable_pokemon_ids:
            if pokemon_id not in self._state.inventory.candies:
                # キャンディーが無いということはポケモンを捕まえていないということ
                continue

            candies = self._state.inventory.candies[pokemon_id]
            pokemons = to_evolve_pokemons[pokemon_id]
            # キャンディーの分進化させ、進化後のポケモンを博士に送る
            while candies // pokedex.evolves[pokemon_id] < len(pokemons):
                pokemon = pokemons.pop()
                log.info("Releasing {}...".format(pokedex[pokemon.pokemon_id]))
                release_result = self._api.release_pokemon(pokemon, delay=delay)
                log.info("Release Result: {}".format(release_result))
                candies += 1

            # アメが足りなく進化できなかったポケモンを博士に送る
            for pokemon in pokemons:
                log.info("Evolving {}...".format(pokedex[pokemon.pokemon_id]))
                evolve_result = self._api.evolve_pokemon(pokemon, delay=delay)
                log.info("Evolve Result: {}".format(evolve_result))
                release_result = self._api.release_pokemon(pokemon, delay=delay)
                log.info("Release Result: {}".format(release_result))

    def clean_inventory(self, delay=5):
        log.info("Cleaning out Inventory...")
        bag = self._state.inventory.bag

        # Clear out all of a crtain type
        tossable_item_ids = [items.POTION, items.SUPER_POTION, items.REVIVE]
        for item_id in tossable_item_ids:
            if item_id in bag and bag[item_id] > 0:
                self._api.recycle_inventory_item(item_id, count=bag[item_id], delay=delay)

        # Limit a certain type
        limited_items = {
            items.POKE_BALL: 50,
            items.GREAT_BALL: 100,
            items.ULTRA_BALL: 150,
            items.RAZZ_BERRY: 25
        }
        for item_id in limited_items:
            if item_id in bag and bag[item_id] > limited_items[item_id]:
                self._api.recycle_inventory_item(item_id, count=(bag[item_id] - limited_items[item_id]), delay=delay)

    def walk_and_catch(self, route):
        # 歩き出す前にポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(route.instance):
            return None

        log.info("Catching {}:".format(pokedex[route.instance.pokemon_id]))
        self.walk_on(route, step=3.2)
        self.encounter_and_catch(route.instance)

    def encounter_and_catch(self, pokemon, threshold_p=0.5, limit=5, delay=2):
        # ポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(pokemon):
            return None

        self._state.catch.start_catching(pokemon)

        # Start encounter
        encounter = self._api.encounter_pokemon(pokemon, delay=delay)

        # If party full
        if encounter.status == 7:  # FIXME Enum使う
            raise GeneralPokemonBotException("Can't catch! Party is full!")

        # Grab needed data from proto
        chances = encounter.capture_probability["capture_probability"]
        balls = encounter.capture_probability["pokeball_type"]
        balls = balls or [items.POKE_BALL, items.GREAT_BALL, items.ULTRA_BALL]
        bag = self._state.inventory.bag

        # Have we used a razz berry yet?
        berried = False

        # Make sure we aren't oer limit
        count = 0

        # Attempt catch
        while True:
            best_ball = items.UNKNOWN
            alt_ball = items.UNKNOWN

            # Check for balls and see if we pass
            # wanted threshold
            print(balls)
            for i, ball in enumerate(balls):
                print(bag.get(ball, 0) > 0)
                if bag.get(ball, 0) > 0:
                    alt_ball = ball
                    if chances[i] > threshold_p:
                        best_ball = ball
                        break

            # If we can't determine a ball, try a berry
            # or use a lower class ball
            if best_ball == items.UNKNOWN:
                if not berried and bag.get(items.RAZZ_BERRY, 0) > 0:
                    log.info("Using a RAZZ_BERRY")
                    self._api.use_item_capture(items.RAZZ_BERRY, pokemon, delay=delay + random.randint(0, 2))
                    berried = True
                    continue

                # if no alt ball, there are no balls
                elif alt_ball == items.UNKNOWN:
                    raise GeneralPokemonBotException("Out of usable balls")
                else:
                    best_ball = alt_ball

            # Try to catch it!!
            log.info("Using a %s" % items[best_ball])
            attempt = self._api.catch_pokemon(pokemon, best_ball, delay=delay + random.randint(0, 2))

            # Success or run away
            if attempt["status"] == 1:
                return attempt

            # CATCH_FLEE is bad news
            if attempt["status"] == 3:
                if count == 0:
                    log.info("Possible soft ban.")
                else:
                    log.info("Pokemon fled at {}th attempt".format(count + 1))
                return attempt

            # Only try up to x attempts
            count += 1
            if count >= limit:
                log.info("Over catch limit")
                return None

    # Walk to fort and spin
    def walk_and_spin(self, route, delay=2):
        details = self._api.get_fort_details(route.instance, delay=delay)
        log.info("Spinning the Fort \"{}\":".format(details.name))

        self.walk_on(route, step=3.2)

        fort_search_result = self._api.get_fort_search(route.instance, delay=delay)
        log.info("Fort Search Result: {}".format(fort_search_result))

    def set_egg(self):
        # If no eggs, nothing we can do
        if len(self._state.inventory.eggs) == 0:
            return None

        egg = self._state.inventory.eggs[0]
        incubator = self._state.inventory.incubators[0]
        return self._api.set_egg(incubator, egg)  # FIXME

    def set_coordinates(self, latitude, longitude):
        self.location.set_position(latitude, longitude)
        self._api.set_coordinates(self.location.position)
        map_objects = self.get_map_objects(radius=1, delay=1)
        log.info(map_objects)
        # TODO 範囲内のポケストップは回す
        # TODO 捕まえられるポケモンは捕まえる
        
    def walk_on(self, route, epsilon=10, step=7.5):
        if route.legs is None:
            self.walk_to(route.instance.latitude,
                         route.instance.longitude,
                         epsilon=epsilon,
                         step=step)
        else:
            for s in route.legs["steps"]:
                self.walk_to(s["end_location"]["lat"],
                             s["end_location"]["lng"],
                             epsilon=epsilon,
                             step=step)

    def walk_to(self, olatitude, olongitude, epsilon=10, step=7.5, delay=10):
        if step >= epsilon:
            raise GeneralPokemonBotException("Walk may never converge")

        # Calculate distance to position
        latitude, longitude, _ = self.location.get_position()
        dist = closest = Location.get_distance(latitude, longitude, olatitude, olongitude)

        # Run walk
        divisions = closest / step
        d_lat = (latitude - olatitude) / divisions
        d_lon = (longitude - olongitude) / divisions

        log.info("Walking {0} meters. This will take ~{1} seconds...".format(dist, dist / step))

        steps = 1
        while dist > epsilon:
            log.info("{} m -> {} m away".format(closest - dist, closest))
            latitude -= d_lat
            longitude -= d_lon
            steps %= delay
            if steps == 0:
                self.set_coordinates(latitude, longitude)
            else:
                time.sleep(1)
            dist = Location.get_distance(latitude, longitude, olatitude, olongitude)
            steps += 1

        # Finalize walk
        steps -= 1
        if steps % delay > 0:
            time.sleep(delay - steps)
            self.set_coordinates(latitude, longitude)
