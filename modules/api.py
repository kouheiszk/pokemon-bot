#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from pgoapi import pgoapi, utilities

from modules.encounter import Encounter
from modules.exceptions import GeneralPokemonBotException
from modules.fort import Fort
from modules.item import items
from modules.location import Location
from modules.utilities import get_encryption_lib_path

log = logging.getLogger("pokemon_bot")


class Api(object):
    def __init__(self, location_lookup=None):
        self.location = Location(location_lookup)

        self._api = pgoapi.PGoApi()
        self._api.set_position(*self.location.get_position())

    def authenticate(self, auth_service, username, password):
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

    def _get_profile(self, state):
        req = self.get_default_request()
        req.get_player()
        response_dict = req.call()

        player_dict = response_dict["responses"]["GET_PLAYER"]["player_data"]
        state.player.parse_response_dic(player_dict)

        eggs_dict = response_dict["responses"]["GET_HATCHED_EGGS"]
        state.eggs.parse_response_dic(eggs_dict)

        inventory_dict = response_dict["responses"]["GET_INVENTORY"]["inventory_delta"]
        state.inventory.parse_response_dic(inventory_dict)

        badges_dict = response_dict["responses"]["CHECK_AWARDED_BADGES"]
        state.badges.parse_response_dic(badges_dict)

        settings_dict = response_dict["responses"]["DOWNLOAD_SETTINGS"]["settings"]
        state.settings.parse_response_dic(settings_dict)

    def get_player(self, state):
        self._get_profile(state)
        return state.player

    def get_eggs(self, state):
        self._get_profile()
        return state.eggs

    def get_inventory(self, state):
        self._get_profile(state)
        return state.inventory

    def get_badges(self, state):
        self._get_profile(state)
        return state.badges

    def get_settings(self, state):
        self._get_profile(state)
        return state.settings

    def get_map_objects(self, state, radius=1000):
        cell_ids = self.location.get_cell_ids(radius=radius)
        timestamps = [0, ] * len(cell_ids)
        response_dict = self._api.get_map_objects(latitude=utilities.f2i(self.location.latitude),
                                                  longitude=utilities.f2i(self.location.longitude),
                                                  since_timestamp_ms=timestamps,
                                                  cell_id=cell_ids)
        map_objects_dict = response_dict["responses"]["GET_MAP_OBJECTS"]
        state.map_objects.parse_response_dic(map_objects_dict)
        return state.map_objects

    def release_pokemon(self, pokemon):
        response_dict = self._api.release_pokemon(pokemon_id=pokemon.id)
        log.debug("Response dictionary (release_pokemon): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def evolve_pokemon(self, pokemon):
        response_dict = self._api.evolve_pokemon(pokemon_id=pokemon.id)
        log.info("Response dictionary (evolve_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def recycle_inventory_item(self, item_id, count=0):
        if count > 0:
            response_dict = self._api.recycle_inventory_item(item_id=item_id, count=count)
        else:
            response_dict = None
        log.debug("Response dictionary (recycle_inventory_item): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def encounter_pokemon(self, pokemon):
        response_dict = self._api.encounter(encounter_id=pokemon.encounter_id,
                                            spawn_point_id=pokemon.spawn_point_id,
                                            player_latitude=self.location.latitude,
                                            player_longitude=self.location.altitude)
        encounter = response_dict["responses"]["ENCOUNTER"]
        log.info("Response dictionary (encounter): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(encounter)))
        return Encounter(encounter)

    def use_item_capture(self, item_id, pokemon):
        response_dict = self._api.use_item_capture(item_id=item_id,
                                                   encounter_id=pokemon.encounter_id,
                                                   spawn_point_id=pokemon.spawn_point_id)
        return response_dict

    def catch_pokemon(self, pokemon, pokeball=items.POKE_BALL, normalized_reticle_size=1.950, hit_pokemon=True,
                      spin_modifier=0.850, normalized_hit_position=1.0):
        response_dict = self._api.catch_pokemon(encounter_id=pokemon.encounter_id,
                                                pokeball=pokeball,
                                                normalized_reticle_size=normalized_reticle_size,
                                                spawn_point_id=pokemon.spawn_point_id,
                                                hit_pokemon=hit_pokemon,
                                                spin_modifier=spin_modifier,
                                                normalized_hit_position=normalized_hit_position)
        log.info("Response dictionary (catch_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def get_fort_details(self, fort):
        response_dict = self._api.fort_details(fort_id=fort.id,
                                               latitude=fort.latitude,
                                               longitude=fort.longitude)
        fort_dict = response_dict["responses"]["FORT_DETAILS"]
        log.debug("Response dictionary (fort_details): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(fort_dict)))
        return Fort(fort_dict)

    def get_fort_search(self, fort):
        response_dict = self._api.fort_search(fort_id=fort.id,
                                              player_latitude=self.location.latitude,
                                              player_longitude=self.location.longitude,
                                              fort_latitude=fort.latitude,
                                              fort_longitude=fort.longitude)
        return response_dict

    def set_coordinates(self, latitude, longitude):
        self.location.set_position(latitude, longitude)
        self.get_map_objects(radius=1)
