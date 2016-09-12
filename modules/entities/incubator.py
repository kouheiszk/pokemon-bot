#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from modules.item import Item

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

    def __str__(self):
        if self.uses_remaining:
            return "{}（あと{}回）".format(Item.INCUBATOR_BASIC, self.uses_remaining)
        else:
            return "{}".format(Item.INCUBATOR_BASIC_UNLIMITED)
