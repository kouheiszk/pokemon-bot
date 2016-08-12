#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

import sys

import time
from pgoapi import pgoapi, utilities

from modules.exceptions import GeneralPokemonBotException
from modules.fort import Fort
from modules.item import items
from modules.location import Location
from modules.state import State
from modules.utilities import get_encryption_lib_path

log = logging.getLogger(__name__)


class Api(object):
    def __init__(self, locationLookup=None):
        self.location = Location(locationLookup)

        self._api = pgoapi.PGoApi()
        self._api.set_position(*self.location.get_position())

        self._state = State()

    def authenticate(self, auth_service, username, password):
        # # ログインする
        # if not self._api.login(auth_service, username, password, app_simulation=True):
        #     raise GeneralPokemonBotException("Invalid Authentication Info")

        # Check if we have the proper encryption library file and get its path
        encryption_lib_path = get_encryption_lib_path()
        if encryption_lib_path is "":
            raise GeneralPokemonBotException("Encryption library file is required")

        self._api.set_authentication(provider=auth_service, username=username, password=password)

        # provide the path for your encrypt dll
        self._api.activate_signature(encryption_lib_path)

    def get_default_request(self):
        req = self._api.create_request()
        req.get_hatched_eggs()
        req.get_inventory()
        req.check_awarded_badges()
        req.download_settings()
        return req

    def parse_default_request_response(self, response_dict):
        self._state.eggs.parse_response_dic(response_dict)
        self._state.inventory.parse_response_dic(response_dict)
        self._state.badges.parse_response_dic(response_dict)
        self._state.settings.parse_response_dic(response_dict)

    def get_profile(self):
        req = self.get_default_request()
        req.get_player()
        response_dict = req.call()
        self._state.player.parse_response_dic(response_dict)
        self.parse_default_request_response(response_dict)

    def get_player(self):
        self.get_profile()
        return self._state.player

    def get_eggs(self):
        self.get_profile()
        return self._state.eggs

    def get_inventory(self):
        self.get_profile()
        return self._state.inventory

    def get_badges(self):
        self.get_profile()
        return self._state.badges

    def get_settings(self):
        self.get_profile()
        return self._state.settings

    def get_map_objects(self, radius=1000):
        cell_ids = self.location.get_cell_ids(radius=radius)
        timestamps = [0, ] * len(cell_ids)
        response_dict = self._api.get_map_objects(latitude=utilities.f2i(self.location.latitude),
                                                  longitude=utilities.f2i(self.location.longitude),
                                                  since_timestamp_ms=timestamps,
                                                  cell_id=cell_ids)
        self._state.map_objects.parse_response_dic(response_dict)
        return self._state.map_objects

    def release_pokemon(self, pokemon):
        response_dict = self._api.release_pokemon(pokemon_id=pokemon.get("pokemon_id"))
        return response_dict

    def evolve_pokemon(self, pokemon):
        response_dict = self._api.evolve_pokemon(pokemon_id=pokemon.get("pokemon_id"))
        return response_dict

    def recycle_inventory_item(self, item_id, count=0):
        if count > 0:
            response_dict = self._api.recycle_inventory_item(item_id=item_id, count=count)
        else:
            response_dict = None
        return response_dict

    def encounter_pokemon(self, pokemon):
        response_dict = self._api.encounter(encounter_id=pokemon.get("encounter_id"),
                                            spawn_point_id=pokemon.get("spawn_point_id"),
                                            player_latitude=self.location.latitude,
                                            player_longitude=self.location.altitude)

        log.info("Response dictionary (encounter): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        sys.exit(1)

        return response_dict

    def use_item_capture(self, item_id, pokemon):
        response_dict = self._api.use_item_capture(item_id=item_id,
                                                   encounter_id=pokemon.get("encounter_id"),
                                                   spawn_point_id=pokemon.get("spawn_point_id"))
        return response_dict

    def catch_pokemon(self, pokemon, pokeball=items.POKE_BALL, normalized_reticle_size=1.950, hit_pokemon=True,
                      spin_modifier=0.850, normalized_hit_position=1.0):
        response_dict = self._api.catch_pokemon(encounter_id=pokemon.get("encounter_id"),
                                                pokeball=pokeball,
                                                normalized_reticle_size=normalized_reticle_size,
                                                spawn_point_id=pokemon.get("spawn_point_id"),
                                                hit_pokemon=hit_pokemon,
                                                spin_modifier=spin_modifier,
                                                normalized_hit_position=normalized_hit_position)

        log.info("Response dictionary (catch_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        sys.exit(1)

        return response_dict

    def get_fort_details(self, fort):
        response_dict = self._api.fort_details(fort_id=fort.get("id"),
                                               latitude=fort.get("latitude"),
                                               longitude=fort.get("longitude"))
        fort = Fort()
        fort.parse_response_dic(response_dict)
        return fort

    def get_fort_search(self, fort):
        response_dict = self._api.fort_search(fort_id=fort.get("id"),
                                              player_latitude=self.location.latitude,
                                              player_longitude=self.location.longitude,
                                              fort_latitude=fort.get("latitude"),
                                              fort_longitude=fort.get("longitude"))
        return response_dict

    def set_coordinates(self, latitude, longitude):
        self.location.set_position(latitude, longitude)
        self.get_map_objects(radius=1)

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
