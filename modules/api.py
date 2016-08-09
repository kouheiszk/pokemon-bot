#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from pgoapi import pgoapi

from modules.exceptions import GeneralPokemonBotException
from modules.location import Location
from modules.player import Player
from modules.state import State

log = logging.getLogger(__name__)


class Api(object):
    def __init__(self, locationLookup=None):
        location = Location(locationLookup)

        self._api = pgoapi.PGoApi()
        self._api.set_position(*location.get_position())

        self._state = State()

    def authenticate(self, auth_service, username, password):
        # ログインする
        if not self._api.login(auth_service, username, password, app_simulation=True):
            raise GeneralPokemonBotException("Invalid Authentication Info")

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
