#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from pgoapi import utilities
from s2sphere import CellId, LatLng

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

    def set_postioin_by_name(self, location_lookup):
        position = utilities.get_pos_by_name(location_lookup)
        self.latitude, self.longitude, self.altitude = position

    def set_position(self, latitude, longitude, altitude=0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def get_position(self):
        return self.latitude, self.longitude, self.altitude

    def get_cell_ids(self):
        return utilities.get_cell_ids(self.latitude, self.longitude)
