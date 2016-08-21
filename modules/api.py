#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

import time

from pgoapi import pgoapi, utilities

from modules.encounter import Encounter
from modules.exceptions import GeneralPokemonBotException
from modules.fort import Fort
from modules.item import items
from modules.utilities import get_encryption_lib_path

log = logging.getLogger("pokemon_bot")


class Api(object):
    def __init__(self, location):
        self._location = location
        self._api = pgoapi.PGoApi()
        self._api.set_position(*location.position)
        self._available_time = time.time()

    def _create_request(self, defaults=True, delay=1):
        # 前回のリクエスト終了から、次回リクエスト実行までの間隔をあける
        delta = int(self._available_time - time.time())
        if delta > 0:
            print("\rCooldown... {}sec to do...".format(delta))
            time.sleep(delta)

        self._available_time = time.time() + delay

        # リクエスト作成
        req = self._api.create_request()

        # リクエストに通常のリクエストをラップ
        if defaults:
            req.get_hatched_eggs()
            req.get_inventory()
            req.check_awarded_badges()
            req.download_settings()

        return req

    def authenticate(self, auth_service, username, password):
        # Check if we have the proper encryption library file and get its path
        encryption_lib_path = get_encryption_lib_path()
        if encryption_lib_path is "":
            raise GeneralPokemonBotException("Encryption library file is required")

        self._api.set_authentication(provider=auth_service, username=username, password=password)

        # provide the path for your encrypt dll
        self._api.activate_signature(encryption_lib_path)

    def _get_profile(self, state, delay=10):
        req = self._create_request(delay=delay)
        req.get_player()
        response_dict = req.call()

        player_dict = response_dict["responses"]["GET_PLAYER"]["player_data"]
        state.player.parse_response_dic(player_dict)

        eggs_dict = response_dict["responses"]["GET_HATCHED_EGGS"]
        state.hatched_eggs.parse_response_dic(eggs_dict)

        inventory_dict = response_dict["responses"]["GET_INVENTORY"]["inventory_delta"]
        state.inventory.parse_response_dic(inventory_dict)

        badges_dict = response_dict["responses"]["CHECK_AWARDED_BADGES"]
        state.badges.parse_response_dic(badges_dict)

        settings_dict = response_dict["responses"]["DOWNLOAD_SETTINGS"]["settings"]
        state.settings.parse_response_dic(settings_dict)

    def get_player(self, state, delay=10):
        log.info("Call GET_PLAYER...")
        self._get_profile(state, delay=delay)
        return state.player

    def get_eggs(self, state, delay=10):
        log.info("Call GET_HATCHED_EGGS...")
        self._get_profile(state, delay=delay)
        return state.eggs

    def get_inventory(self, state, delay=10):
        log.info("Call GET_INVENTORY...")
        self._get_profile(state, delay=delay)
        return state.inventory

    def get_badges(self, state, delay=10):
        log.info("Call CHECK_AWARDED_BADGES...")
        self._get_profile(state, delay=delay)
        return state.badges

    def get_settings(self, state, delay=10):
        log.info("Call DOWNLOAD_SETTINGS...")
        self._get_profile(state, delay=delay)
        return state.settings

    def get_map_objects(self, state, cell_ids, delay=10):
        log.info("Call GET_MAP_OBJECTS...")
        req = self._create_request(delay=delay)
        req.get_map_objects(latitude=utilities.f2i(self._location.latitude),
                            longitude=utilities.f2i(self._location.longitude),
                            since_timestamp_ms=[0, ] * len(cell_ids),
                            cell_id=cell_ids)
        response_dict = req.call()
        map_objects_dict = response_dict["responses"]["GET_MAP_OBJECTS"]
        state.map_objects.parse_response_dic(map_objects_dict)
        return state.map_objects

    def release_pokemon(self, pokemon, delay=10):
        log.info("Call RELEASE_POKEMON...")
        req = self._create_request(defaults=False, delay=delay)
        req.release_pokemon(pokemon_id=pokemon.id)
        response_dict = req.call()
        log.info("Response dictionary (release_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def evolve_pokemon(self, pokemon, delay=10):
        log.info("Call EVOLVE_POKEMON...")
        req = self._create_request(delay=delay)
        req.evolve_pokemon(pokemon_id=pokemon.id)
        response_dict = req.call()
        log.info("Response dictionary (evolve_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def recycle_inventory_item(self, item_id, count=0, delay=10):
        log.info("Call RECYCLE_INVNETORY_ITEM...")
        req = self._create_request(delay=delay)
        if count > 0:
            req.recycle_inventory_item(item_id=item_id, count=count)
            response_dict = req.call()
        else:
            response_dict = None
        log.info("Response dictionary (recycle_inventory_item): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def encounter_pokemon(self, pokemon, delay=10):
        log.info("Call ENCOUNTER...")
        req = self._create_request(delay=delay)
        req.encounter(encounter_id=pokemon.encounter_id,
                      spawn_point_id=pokemon.spawn_point_id,
                      player_latitude=self._location.latitude,
                      player_longitude=self._location.altitude)
        response_dict = req.call()
        encounter = response_dict["responses"]["ENCOUNTER"]
        log.info("Response dictionary (encounter): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(encounter)))
        return Encounter(encounter)

    def use_item_capture(self, item_id, pokemon, delay=10):
        log.info("Call ITEM_CAPTURE...")
        req = self._create_request(defaults=False, delay=delay)
        req.use_item_capture(item_id=item_id,
                             encounter_id=pokemon.encounter_id,
                             spawn_point_id=pokemon.spawn_point_id)
        response_dict = req.call()
        log.info("Response dictionary (use_item_capture): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def catch_pokemon(self, pokemon, pokeball=items.POKE_BALL,
                      normalized_reticle_size=1.950,
                      hit_pokemon=True,
                      spin_modifier=0.850,
                      normalized_hit_position=1.0,
                      delay=10):
        log.info("Call CATCH_POKEMON...")
        req = self._create_request(delay=delay)
        req.catch_pokemon(encounter_id=pokemon.encounter_id,
                          pokeball=pokeball,
                          normalized_reticle_size=normalized_reticle_size,
                          spawn_point_id=pokemon.spawn_point_id,
                          hit_pokemon=hit_pokemon,
                          spin_modifier=spin_modifier,
                          normalized_hit_position=normalized_hit_position)
        response_dict = req.call()
        catch_pokemon_dict = response_dict["responses"]["CATCH_POKEMON"]
        log.info("Response dictionary (catch_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(catch_pokemon_dict)))
        return catch_pokemon_dict

    def get_fort_details(self, fort, delay=2):
        log.info("Call FORT_DETAILS...")
        req = self._create_request(delay=delay)
        req.fort_details(fort_id=fort.id,
                         latitude=fort.latitude,
                         longitude=fort.longitude)
        response_dict = req.call()
        fort_dict = response_dict["responses"]["FORT_DETAILS"]
        log.debug("Response dictionary (fort_details): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(fort_dict)))
        return Fort(fort_dict)

    def get_fort_search(self, fort, delay=2):
        log.info("Call FORT_SEARCH...")
        req = self._create_request(delay=delay)
        req.fort_search(fort_id=fort.id,
                        player_latitude=self._location.latitude,
                        player_longitude=self._location.longitude,
                        fort_latitude=fort.latitude,
                        fort_longitude=fort.longitude)
        response_dict = req.call()
        fort_search_dict = response_dict["responses"]["FORT_SEARCH"]
        return fort_search_dict

    def set_coordinates(self, position):
        self._api.set_position(*position)
