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

    def get_player(self):
        response_dict = self._api.get_player()
        self._state.player.parse_response_dic(response_dict)
        return self._state.player

    def get_inventory(self):
        response_dict = self._api.get_inventory()
        self._state.inventory.parse_response_dic(response_dict)
        return self._state.inventory
