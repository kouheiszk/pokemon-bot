#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import time

import sys

from modules.api import Api
from modules.exceptions import GeneralPokemonBotException
from modules.item import items
from modules.location import Location
from modules.pokedex import pokedex
from modules.state import State

log = logging.getLogger("pokemon_bot")


class Session(object):
    def __init__(self, location_lookup=None):
        self._api = Api(location_lookup)
        self._state = State()

    def authenticate(self, auth_service, username, password, delay=5):
        log.info("Authenticate with {}...".format(auth_service))
        self._api.authenticate(auth_service, username, password)
        time.sleep(delay)

    def get_inventory(self, delay=10):
        log.info("Get Inventory...")
        self._api.get_inventory(self._state)
        time.sleep(delay)
        return self._state.inventory

    def get_map_objects(self, delay=10):
        log.info("Get Map Objects...")
        self._api.get_map_objects(self._state)
        time.sleep(delay)
        return self._state.map_objects

    def walk_and_catch_and_spin(self, map_objects, catch=True, spin=True):
        if catch:
            log.info("Catch Pokemons...")
            for pokemon in map_objects.catchable_pokemons:
                self.walk_and_catch(pokemon)

            for pokemon in map_objects.wild_pokemons:
                self.walk_and_catch(pokemon)

            log.info(map_objects.catchable_pokemons)

        if spin:
            log.info("Spin Pokestops...")
            for pokestop in map_objects.sort_close_pokestops(self._api.location):
                self.walk_and_spin(pokestop)

                sys.exit(0)

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
                self._api.release_pokemon(pokemon)
                time.sleep(delay)

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
                self._api.release_pokemon(pokemon)
                time.sleep(delay)
                candies += 1

            # アメが足りなく進化できなかったポケモンを博士に送る
            for pokemon in pokemons:
                log.info("Evolving {}...".format(pokedex[pokemon.pokemon_id]))
                log.info(self._api.evolve_pokemon(pokemon))
                time.sleep(delay)
                self._api.release_pokemon(pokemon)
                time.sleep(delay)

    def clean_inventory(self, delay=5):
        log.info("Cleaning out Inventory...")
        bag = self._state.inventory.bag

        # Clear out all of a crtain type
        tossable_item_ids = [items.POTION, items.SUPER_POTION, items.REVIVE]
        for item_id in tossable_item_ids:
            if item_id in bag and bag[item_id] > 0:
                self._api.recycle_inventory_item(item_id, count=bag[item_id])
                time.sleep(delay)

        # Limit a certain type
        limited_items = {
            items.POKE_BALL: 50,
            items.GREAT_BALL: 100,
            items.ULTRA_BALL: 150,
            items.RAZZ_BERRY: 25
        }
        for item_id in limited_items:
            if item_id in bag and bag[item_id] > limited_items[item_id]:
                self._api.recycle_inventory_item(item_id, count=(bag[item_id] - limited_items[item_id]))
                time.sleep(delay)

    def walk_and_catch(self, pokemon, delay=2):
        # 歩き出す前にポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(pokemon):
            return None

        if pokemon:
            log.info("Catching {}:".format(pokedex[pokemon.pokemon_id]))
            self.walk_to(pokemon.latitude, pokemon.longitude, step=3.2)
            time.sleep(delay)
            result = self.encounter_and_catch(pokemon, self._state.inventory)
            log.info(result)
            return result
        else:
            return None

    def encounter_and_catch(self, pokemon, inventory, threshold_p=0.5, limit=5, delay=2):
        # ポケモンを捕まえられるかチェック
        if not self._state.catch.is_catchable_pokemon(pokemon):
            return None

        self._state.catch.start_catching(pokemon)

        # Start encounter
        encounter = self._api.encounter_pokemon(pokemon)
        time.sleep(delay)

        # If party full
        if encounter.status == encounter.POKEMON_INVENTORY_FULL:
            raise GeneralPokemonBotException("Can't catch! Party is full!")

        # Grab needed data from proto
        chances = encounter.capture_probability.capture_probability
        balls = encounter.capture_probability.pokeball_type
        balls = balls or [items.POKE_BALL, items.GREAT_BALL, items.ULTRA_BALL]
        bag = inventory.bag

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
                    logging.info("Using a RAZZ_BERRY")
                    self._api.use_item_capture(items.RAZZ_BERRY, pokemon)
                    berried = True
                    time.sleep(delay + random.randint(1, 3))
                    continue

                # if no alt ball, there are no balls
                elif alt_ball == items.UNKNOWN:
                    raise GeneralPokemonBotException("Out of usable balls")
                else:
                    best_ball = alt_ball

            # Try to catch it!!
            log.info("Using a %s" % items[best_ball])
            attempt = self._api.catch_pokemon(pokemon, best_ball)
            time.sleep(delay)

            # Success or run away
            if attempt.status == 1:
                return attempt

            # CATCH_FLEE is bad news
            if attempt.status == 3:
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
    def walk_and_spin(self, pokestop, delay=2):
        if pokestop:
            details = self._api.get_fort_details(pokestop)
            log.info("Spinning the Fort \"{}\":".format(details.name))
            time.sleep(delay)

            self._api.walk_to(pokestop.get("latitude"), pokestop.get("longitude"), step=3.2)
            time.sleep(delay)

            log.info(self._api.get_fort_search(pokestop))
            time.sleep(delay)

    def set_egg(self):
        # If no eggs, nothing we can do
        if len(self._state.inventory.eggs) == 0:
            return None

        egg = self._state.inventory.eggs[0]
        incubator = self._state.inventory.incubators[0]
        return self._api.set_egg(incubator, egg)  # FIXME

    # ゆっくり歩く
    def walk_to(self, olatitude, olongitude, epsilon=10, step=7.5, delay=10):
        # TODO 卵をチェックする

        if step >= epsilon:
            raise GeneralPokemonBotException("Walk may never converge")

        # Calculate distance to position
        latitude, longitude, _ = self._state.location.get_position()
        dist = closest = Location.get_distance(latitude, longitude, olatitude, olongitude)

        # Run walk
        divisions = closest / step
        d_lat = (latitude - olatitude) / divisions
        d_lon = (longitude - olongitude) / divisions

        log.info("Walking {0} meters. This will take ~{1} seconds...".format(dist, dist / step))

        steps = 1
        while dist > epsilon:
            log.debug("{} m -> {} m away".format(closest - dist, closest))
            latitude -= d_lat
            longitude -= d_lon
            steps %= delay
            if steps == 0:
                self._state.location.set_position(latitude, longitude)
            time.sleep(1)
            dist = Location.get_distance(latitude, longitude, olatitude, olongitude)
            steps += 1

        # Finalize walk
        steps -= 1
        if steps % delay > 0:
            time.sleep(delay - steps)
            self._state.location.set_position(latitude, longitude)
