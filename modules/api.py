#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from pgoapi import pgoapi, utilities

from modules.exceptions import GeneralPokemonBotException
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

    def get_map_objects(self):
        cell_ids = self.location.get_cell_ids()
        timestamps = [0, ] * len(cell_ids)
        response_dict = self._api.get_map_objects(latitude=utilities.f2i(self.location.latitude),
                                                  longitude=utilities.f2i(self.location.longitude),
                                                  since_timestamp_ms=timestamps,
                                                  cell_id=cell_ids)
        self._state.map_objects.parse_response_dic(response_dict)
        return self._state.map_objects
