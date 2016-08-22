#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Encounter(object):
    def __init__(self, d):
        self.__dict__.update(d)

    @property
    def capture_probability(self):
        return self.__dict__.get("capture_probability", {})
