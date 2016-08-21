#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Encounter(object):
    def __init__(self, d):
        self.__dict__.update(d)

    def is_enable_catch(self):
        if self.status == 1:
            return True
        else:
            return False

    def capture_probability(self):
        return self.__dict__.get("capture_probability", {})
