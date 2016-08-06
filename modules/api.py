#!/usr/bin/python
# -*- coding: utf-8 -*-

from pgoapi import pgoapi

from modules.exceptions import GeneralPokemonBotException
from modules.location import Location


class Api(object):
    def __init__(self, locationLookup=None):
        self.api = pgoapi.PGoApi()

        location = Location(locationLookup)
        self.api.set_position(*location.get_position())

    def authenticate(self, auth_service, username, password):
        # ログインする
        if not self.api.login(auth_service, username, password, app_simulation=True):
            raise GeneralPokemonBotException("Invalid Authentication Info")
