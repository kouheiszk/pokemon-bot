#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging

import urllib

log = logging.getLogger("pokemon_bot")


class Route(object):
    def __init__(self, instance, legs=None):
        self.instance = instance
        self.legs = legs

    @classmethod
    def create_routes(cls, positions):
        if len(positions) < 2:
            return [cls(p) for p in positions]

        routes_url = cls._create_routes_request_url(positions)
        routes_data = cls._get_routes_data(routes_url)
        waypoint_count = len(routes_data["waypoint_order"])

        routes = []
        routes.append(cls(positions[0]))
        for i in range(len(routes_data["legs"])):
            legs = routes_data["legs"][i]
            index = routes_data["waypoint_order"][i] if i < waypoint_count else waypoint_count
            position = positions[index + 1]
            routes.append(cls(position, legs))

        return routes

    @classmethod
    def _create_routes_request_url(cls, positions):
        start = "{},{}".format(positions[0].latitude, positions[0].longitude)
        end = "{},{}".format(positions[-1].latitude, positions[-1].longitude)
        routes = ""
        for position in positions[1:-1]:
            routes += "{},{}|".format(position.latitude, position.longitude)
        routes_url = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints={}".format(
            start, end, routes[:-1])
        return routes_url

    @classmethod
    def _get_routes_data(cls, routes_request_url):
        log.info("Request Routes...")
        log.info("Request: {}".format(routes_request_url))
        response = urllib.request.urlopen(routes_request_url)
        data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        routes_data = data["routes"][0]

        leg_routes = ""
        for leg in routes_data["legs"]:
            for step in leg["steps"]:
                leg_routes += "{},{}|{},{}|".format(step["start_location"]["lat"], step["start_location"]["lng"],
                                                    step["end_location"]["lat"], step["end_location"]["lng"])

        debug_url = "http://maps.googleapis.com/maps/api/staticmap?size=400x400&path={}".format(leg_routes[:-1])
        log.info("Routes: \n{}".format(debug_url))

        return routes_data
