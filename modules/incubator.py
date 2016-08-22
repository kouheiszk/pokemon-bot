#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Incubator(object):
    def __init__(self, d):
        self.__dict__.update(d)

    @property
    def uses_remaining(self):
        return self.__dict__.get("uses_remaining", None)

    @property
    def pokemon_id(self):
        return self.__dict__.get("pokemon_id", None)
