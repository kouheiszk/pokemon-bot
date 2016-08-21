#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import gpxpy.geo
from pgoapi import utilities
from s2sphere import CellId, LatLng

from modules.exceptions import GeneralPokemonBotException

log = logging.getLogger("pokemon_bot")


class Location(object):
    def __init__(self, location_lookup=None):
        # 位置情報のパース
        position = utilities.get_pos_by_name(location_lookup)
        if not position:
            raise GeneralPokemonBotException("Your given location could not be found by name")

        self.latitude, self.longitude, self.altitude = position

    @property
    def position(self):
        return self.get_position()

    def set_postioin_by_name(self, location_lookup):
        position = utilities.get_pos_by_name(location_lookup)
        self.set_position(*position)

    def set_position(self, latitude, longitude, altitude=0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

        log.info('Coordinates: lat:{}, lng:{}, alt:{}'.format(self.latitude, self.longitude, self.altitude))

    def get_position(self):
        return self.latitude + random.uniform(-0.0000005, 0.0000005), \
               self.longitude + random.uniform(-0.0000005, 0.0000005), \
               self.altitude

    def get_cell_ids(self, radius=10, both_direction=True):
        # Max values allowed by server according to this comment:
        # https://github.com/AeonLucid/POGOProtos/issues/83#issuecomment-235612285
        if radius > 1500:
            radius = 1500  # radius = 1500 is max allowed by the server

        origin = CellId.from_lat_lng(
            LatLng.from_degrees(
                self.latitude,
                self.longitude
            )
        ).parent(15)

        # Create walk around area
        walk = [origin.id()]
        right = origin.next()
        left = origin.prev()

        # Double the radius if we're only walking one way
        if not both_direction:
            radius *= 2

        # Search around provided radius
        for _ in range(radius):
            walk.append(right.id())
            right = right.next()
            if both_direction:
                walk.append(left.id())
                left = left.prev()

        return sorted(walk[:100])  # len(cells) = 100 is max allowed by the server

    @staticmethod
    def get_distance(*coords):
        return gpxpy.geo.haversine_distance(*coords)

    @staticmethod
    def get_lat_long_index(latitude, longitude):
        return CellId.from_lat_lng(
            LatLng.from_degrees(
                latitude,
                longitude
            )
        ).id()
