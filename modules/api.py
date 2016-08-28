#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint
import time

from pgoapi import pgoapi, utilities

from modules.entities.encounter import Encounter
from modules.entities.fort import Fort
from modules.entities.level_up_rewards import LevelUpRewards
from modules.exceptions import GeneralPokemonBotException
from modules.item import Item
from modules.utilities import get_encryption_lib_path

log = logging.getLogger("pokemon_bot")


class Api(object):
    def __init__(self, auth_service, username, password, location):
        self._location = location
        self._requester = ApiRequester(auth_service, username, password, position=location.position)

    def get_player(self, state, delay=10):
        log.debug("Call GET_PLAYER...")
        response_dict = self._requester.get_player(state, delay=delay)
        player_dict = response_dict["responses"]["GET_PLAYER"]["player_data"]
        state.player.parse_response_dic(player_dict)
        return state.player

    def get_map_objects(self, state, cell_ids, delay=10):
        log.debug("Call GET_MAP_OBJECTS...")
        response_dict = self._requester.get_map_objects(state, delay=delay,
                                                        latitude=utilities.f2i(self._location.latitude),
                                                        longitude=utilities.f2i(self._location.longitude),
                                                        since_timestamp_ms=[0, ] * len(cell_ids),
                                                        cell_id=cell_ids)
        map_objects_dict = response_dict["responses"]["GET_MAP_OBJECTS"]
        log.debug("Response dictionary (get_map_objects): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(map_objects_dict)))
        state.map_objects.parse_response_dic(map_objects_dict)
        return state.map_objects

    def release_pokemon(self, pokemon, delay=10):
        log.debug("Call RELEASE_POKEMON...")
        response_dict = self._requester.release_pokemon(defaults=False, delay=delay,
                                                        pokemon_id=pokemon.id)
        release_pokemon_dict = response_dict["responses"]["RELEASE_POKEMON"]
        log.debug("Response dictionary (release_pokemon): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(release_pokemon_dict)))
        return release_pokemon_dict

    def evolve_pokemon(self, state, pokemon, delay=10):
        log.info("Call EVOLVE_POKEMON...")
        response_dict = self._requester.evolve_pokemon(state, delay=delay,
                                                       pokemon_id=pokemon.id)
        log.info("Response dictionary (evolve_pokemon): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))
        return response_dict

    def recycle_inventory_item(self, state, item_id, count=0, delay=10):
        log.debug("Call RECYCLE_INVNETORY_ITEM...")
        if count > 0:
            response_dict = self._requester.recycle_inventory_item(state, delay=delay,
                                                                   item_id=item_id,
                                                                   count=count)
            recycle_inventory_item_dict = response_dict["responses"]["RECYCLE_INVENTORY_ITEM"]
        else:
            recycle_inventory_item_dict = None
        log.debug("Response dictionary (recycle_inventory_item): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(recycle_inventory_item_dict)))
        return recycle_inventory_item_dict

    def encounter_pokemon(self, state, pokemon, delay=10):
        log.debug("Call ENCOUNTER...")
        response_dict = self._requester.encounter(state, delay=delay,
                                                  encounter_id=pokemon.encounter_id,
                                                  spawn_point_id=pokemon.spawn_point_id,
                                                  player_latitude=self._location.latitude,
                                                  player_longitude=self._location.altitude)
        encounter_dict = response_dict["responses"]["ENCOUNTER"]
        log.debug("Response dictionary (encounter): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(encounter_dict)))
        return Encounter(pokemon, encounter_dict)

    def use_item_capture(self, item_id, pokemon, delay=10):
        log.info("Call USE_ITEM_CAPTURE...")
        response_dict = self._requester.use_item_capture(defaults=False, delay=delay,
                                                         item_id=item_id,
                                                         encounter_id=pokemon.encounter_id,
                                                         spawn_point_id=pokemon.spawn_point_id)
        use_item_capture_dict = response_dict["responses"]["USE_ITEM_CAPTURE"]
        log.info("Response dictionary (use_item_capture): \n\r{}"
                 .format(pprint.PrettyPrinter(indent=4).pformat(use_item_capture_dict)))
        return use_item_capture_dict

    def catch_pokemon(self, state, pokemon,
                      pokeball=Item.POKE_BALL,
                      normalized_reticle_size=1.950,
                      hit_pokemon=True,
                      spin_modifier=0.850,
                      normalized_hit_position=1.0,
                      delay=10):
        log.debug("Call CATCH_POKEMON...")
        response_dict = self._requester.catch_pokemon(state, delay=delay,
                                                      encounter_id=pokemon.encounter_id,
                                                      pokeball=pokeball,
                                                      normalized_reticle_size=normalized_reticle_size,
                                                      spawn_point_id=pokemon.spawn_point_id,
                                                      hit_pokemon=hit_pokemon,
                                                      spin_modifier=spin_modifier,
                                                      normalized_hit_position=normalized_hit_position)
        catch_pokemon_dict = response_dict["responses"]["CATCH_POKEMON"]
        log.debug("Response dictionary (catch_pokemon): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(catch_pokemon_dict)))
        return catch_pokemon_dict

    def get_fort_details(self, state, fort, delay=5):
        log.debug("Call FORT_DETAILS...")
        response_dict = self._requester.fort_details(state, delay=delay,
                                                     fort_id=fort.id,
                                                     latitude=fort.latitude,
                                                     longitude=fort.longitude)
        fort_dict = response_dict["responses"]["FORT_DETAILS"]
        log.debug("Response dictionary (fort_details): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(fort_dict)))
        return Fort(fort_dict)

    def get_fort_search(self, state, fort, delay=5):
        log.debug("Call FORT_SEARCH...")
        response_dict = self._requester.fort_search(state, delay=delay,
                                                    fort_id=fort.id,
                                                    player_latitude=self._location.latitude,
                                                    player_longitude=self._location.longitude,
                                                    fort_latitude=fort.latitude,
                                                    fort_longitude=fort.longitude)
        fort_search_dict = response_dict["responses"]["FORT_SEARCH"]
        log.debug("Response dictionary (fort_search): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(fort_search_dict)))
        return fort_search_dict

    def use_item_egg_incubator(self, state, incubator, egg, delay=10):
        log.debug("Call USE_ITEM_EGG_INCUBAROR...")
        response_dict = self._requester.use_item_egg_incubator(state, delay=delay,
                                                               item_id=incubator.id,
                                                               pokemon_id=egg.id)
        use_item_egg_incubator_dict = response_dict["responses"]["USE_ITEM_EGG_INCUBATOR"]
        log.debug("Response dictionary (use_item_egg_incubator): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(use_item_egg_incubator_dict)))
        return use_item_egg_incubator_dict

    def level_up_rewards(self, state, delay=5):
        log.debug("Call LEVEL_UP_REWARDS...")
        level = state.inventory.stats.level
        response_dict = self._requester.level_up_rewards(defaults=False, delay=delay,
                                                         level=level)
        level_up_rewards_dict = response_dict["responses"]["LEVEL_UP_REWARDS"]
        log.debug("Response dictionary (level_up_rewards): \n\r{}"
                  .format(pprint.PrettyPrinter(indent=4).pformat(level_up_rewards_dict)))
        state.inventory.stats.should_get_level_up_rewarded = False
        level_up_rewards = LevelUpRewards(level, level_up_rewards_dict)
        return level_up_rewards

    def set_coordinates(self, position):
        self._requester.set_position(position)


class ApiRequester(object):
    def __init__(self, auth_service, username, password, position):
        self._request_available_time = time.time()
        self._api = pgoapi.PGoApi()

        self.set_position(position)
        time.sleep(1)

        # Check if we have the proper encryption library file and get its path
        encryption_lib_path = get_encryption_lib_path()
        if encryption_lib_path is "":
            raise GeneralPokemonBotException("Encryption library file is required")

        self._api.set_authentication(provider=auth_service, username=username, password=password)
        time.sleep(3)

        # provide the path for your encrypt dll
        self._api.activate_signature(encryption_lib_path)
        time.sleep(2)

    def set_position(self, position):
        self._api.set_position(*position)

    def _create_request(self, defaults=True, delay=1):
        # 前回のリクエスト終了から、次回リクエスト実行までの間隔をあける
        delta = int(self._request_available_time - time.time())
        if delta > 0:
            log.debug("Cooldown... {}sec to do...".format(delta))
            time.sleep(delta)

        self._request_available_time = time.time() + delay

        # リクエスト作成
        req = self._api.create_request()

        # リクエストに通常のリクエストをラップ
        if defaults:
            req.get_hatched_eggs()
            req.get_inventory()
            req.check_awarded_badges()
            req.download_settings()

        return req

    def __getattr__(self, func):
        def function(state=None, defaults=True, delay=10, **kwargs):
            request = self._create_request(defaults=defaults, delay=delay)
            getattr(request, func)(**kwargs)
            response_dict = request.call()

            if defaults and state is not None:
                eggs_dict = response_dict["responses"]["GET_HATCHED_EGGS"]
                state.hatched_eggs.parse_eggs_dict(eggs_dict)

                inventory_dict = response_dict["responses"]["GET_INVENTORY"]["inventory_delta"]
                state.inventory.parse_inventory_dict(inventory_dict)

                badges_dict = response_dict["responses"]["CHECK_AWARDED_BADGES"]
                state.badges.parse_badges_dict(badges_dict)

                settings_dict = response_dict["responses"]["DOWNLOAD_SETTINGS"]["settings"]
                state.settings.parse_settings_dict(settings_dict)

            return response_dict

        return function
