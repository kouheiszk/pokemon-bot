#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import gpxpy.geo
from pgoapi import utilities

from modules.exceptions import GeneralPokemonBotException

log = logging.getLogger("pokemon_bot")


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
        self.set_position(*position)

    def set_position(self, latitude, longitude, altitude=0):
        self.latitude = latitude + random.uniform(0.00001, 0.00005)
        self.longitude = longitude + random.uniform(0.00001, 0.00005)
        self.altitude = altitude

        log.info('Coordinates: {} {} {}'.format(self.latitude, self.longitude, self.altitude))

    def get_position(self):
        return self.latitude, self.longitude, self.altitude

    def get_cell_ids(self, radius=1000):
        return utilities.get_cell_ids(self.latitude, self.longitude, radius)

    @staticmethod
    def get_distance(*coords):
        return gpxpy.geo.haversine_distance(*coords)
