#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import time

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

    def clean_pokemon(self, threshold_cp=50, delay=5):
        log.info("Cleaning out Pokemon...")

        evolvable_pokemon_ids = [pokedex.PIDGEY, pokedex.RATTATA, pokedex.ZUBAT]
        to_evolve_pokemons = {pokemon_id: [] for pokemon_id in evolvable_pokemon_ids}

        # 進化コストのかからないポケモン以外を博士に返す
        for pokemon in self._state.inventory.party:
            # 規定のCP以下のポケモンは博士に返す
            if pokemon.cp < threshold_cp:
                # It makes more sense to evolve some,
                # than throw away
                if pokemon.id in evolvable_pokemon_ids:
                    to_evolve_pokemons[pokemon.pokemon_id].append(pokemon)
                    continue

                # Get rid of low CP, low evolve value
                log.info("Releasing {}...".format(pokedex[pokemon.pokemon_id]))
                self._api.release_pokemon(pokemon)
                time.sleep(delay)

        # ポケモンを進化させる
        for pokemon_id in evolvable_pokemon_ids:
            # if we don't have any candies of that type
            # e.g. not caught that pokemon yet
            if pokemon_id not in self._state.inventory.candies:
                continue
            candies = self._state.inventory.candies[pokemon_id]
            pokemons = to_evolve_pokemons[pokemon_id]
            # release for optimal candies
            while candies // pokedex.evolves[pokemon_id] < len(pokemons):
                pokemon = pokemons.pop()
                log.info("Releasing {}...".format(pokedex[pokemon.pokemon_id]))
                self._api.release_pokemon(pokemon)
                time.sleep(delay)
                candies += 1

            # evolve remainder
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
        if pokemon:
            log.info("Catching {}:".format(pokedex[pokemon.pokemon_id]))
            self.walk_to(pokemon.latitude, pokemon.longitude, step=3.2)
            time.sleep(delay)
            result = self.encounter_and_catch(pokemon, self._state.inventory)
            log.info(result)
            return result
        else:
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
        if step >= epsilon:
            raise GeneralPokemonBotException("Walk may never converge")

        # Calculate distance to position
        latitude, longitude, _ = self._state.location.get_position()
        dist = closest = Location.get_distance(latitude, longitude, olatitude, olongitude)

        # Run walk
        divisions = closest / step
        d_lat = (latitude - olatitude) / divisions
        d_lon = (longitude - olongitude) / divisions

        log.info("Walking %f meters. This will take ~%f seconds..." % (dist, dist / step))

        steps = 1
        while dist > epsilon:
            log.debug("%f m -> %f m away", closest - dist, closest)
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
