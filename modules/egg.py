#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Egg(object):
    def __init__(self, d):
        self.__dict__.update(d)

    @property
    def egg_incubator_id(self):
        return self.__dict__.get("egg_incubator_id", None)

    @property
    def egg_km_walked_start(self):
        return self.__dict__.get("egg_km_walked_start", 0)
