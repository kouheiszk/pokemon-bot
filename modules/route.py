#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging

import urllib

log = logging.getLogger("pokemon_bot")


class Route(object):
    def __init__(self, pokestop, legs=None):
        self.pokestop = pokestop
        self.legs = legs

    @classmethod
    def create_routes(cls, pokestops):
        routes_url = cls._create_routes_request_url(pokestops)
        routes_data = cls._get_routes_data(routes_url)
        waypoint_count = len(routes_data["waypoint_order"])

        routes = []
        routes.append(cls(pokestops[0]))
        for i in range(len(routes_data)):
            legs = routes_data["legs"][i]
            index = routes_data["waypoint_order"][i] if i < waypoint_count else waypoint_count
            pokestop = pokestops[index + 1]
            routes.append(cls(pokestop, legs))

        return routes

    @classmethod
    def _create_routes_request_url(cls, pokestops):
        start = "{},{}".format(pokestops[0].latitude, pokestops[0].longitude)
        end = "{},{}".format(pokestops[-1].latitude, pokestops[-1].longitude)
        routes = ""
        for pokestop in pokestops[1:-1]:
            routes += "{},{}|".format(pokestop.latitude, pokestop.longitude)
        routes_url = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints={}".format(
            start, end, routes[:-1])

        return routes_url

    @classmethod
    def _get_routes_data(cls, routes_request_url):
        log.info("Request Routes...")
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
