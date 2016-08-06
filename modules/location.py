#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from pgoapi import utilities

from modules.exceptions import GeneralPokemonBotException

log = logging.getLogger(__name__)


class Location(object):
    def __init__(self, location_lookup=None, test=False):
        # 位置情報のパース
        position = utilities.get_pos_by_name(location_lookup)
        if not position:
            raise GeneralPokemonBotException("Your given location could not be found by name")
        elif test:
            return

        self.latitude, self.longitude, self.altitude = position

    def get_position(self):
        return self.latitude, self.longitude, self.altitude
