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
    def __init__(self, auth_service, username, password, location_lookup=None):
        api = Api(location_lookup)
        api.authenticate(auth_service, username, password)

        self._api = api
        self._state = State(api)

    def clean_pokemon(self, inventory, threshold_cp=50, delay=5):
        logging.info("Cleaning out Pokemon...")

        evolvable_pokemon_ids = [pokedex.PIDGEY, pokedex.RATTATA, pokedex.ZUBAT]
        to_evolve_pokemons = {pokemon_id: [] for pokemon_id in evolvable_pokemon_ids}

        # 進化コストのかからないポケモン以外を博士に返す
        for pokemon in inventory.party:
            # 規定のCP以下のポケモンは博士に返す
            if pokemon.cp < threshold_cp:
                # It makes more sense to evolve some,
                # than throw away
                if pokemon.id in evolvable_pokemon_ids:
                    to_evolve_pokemons[pokemon.id].append(pokemon)
                    continue

                # Get rid of low CP, low evolve value
                log.info("Releasing %s" % pokedex[pokemon.get("pokemon_id")])
                self._api.release_pokemon(pokemon)
                time.sleep(delay)

        # ポケモンを進化させる
        for pokemon_id in evolvable_pokemon_ids:
            # if we don't have any candies of that type
            # e.g. not caught that pokemon yet
            if evolve not in inventory.candies:
                continue
            candies = inventory.candies[pokemon_id]
            pokemons = to_evolve_pokemons[pokemon_id]
            # release for optimal candies
            while candies // pokedex.evolves[pokemon_id] < len(pokemons):
                pokemon = pokemons.pop()
                log.info("Releasing %s" % pokedex[pokemon.get("pokemon_id")])
                self._api.release_pokemon(pokemon)
                time.sleep(delay)
                candies += 1

            # evolve remainder
            for pokemon in pokemons:
                log.info("Evolving %s" % pokedex[pokemon.get("pokemon_id")])
                log.info(self._api.evolve_pokemon(pokemon))
                time.sleep(delay)
                self._api.release_pokemon(pokemon)
                time.sleep(delay)

    def clean_inventory(self, inventory, delay=5):
        log.info("Cleaning out Inventory...")
        bag = inventory.bag

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

    def walk_and_catch(self, pokemon, inventory, delay=2):
        if pokemon:
            log.info("Catching %s:" % pokedex[pokemon.id])
            self.walk_to(pokemon.latitude, pokemon.longitude, step=3.2)
            time.sleep(delay)
            result = self.encounter_and_catch(pokemon, inventory)
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

    def set_egg(self, inventory):
        # If no eggs, nothing we can do
        if len(inventory.eggs) == 0:
            return None

        egg = inventory.eggs[0]
        incubator = inventory.incubators[0]
        return self._api.set_egg(incubator, egg)  # FIXME

    # ゆっくり歩く
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

        log.info("Walking %f meters. This will take ~%f seconds..." % (dist, dist / step))

        steps = 1
        while dist > epsilon:
            log.debug("%f m -> %f m away", closest - dist, closest)
            latitude -= d_lat
            longitude -= d_lon
            steps %= delay
            if steps == 0:
                self.location.set_position(latitude, longitude)
            time.sleep(1)
            dist = Location.get_distance(latitude, longitude, olatitude, olongitude)
            steps += 1

        # Finalize walk
        steps -= 1
        if steps % delay > 0:
            time.sleep(delay - steps)
            self.location.set_position(latitude, longitude)
