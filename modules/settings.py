#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger("pokemon_bot")


class Settings(object):
    def __init__(self, d={}):
        self.__dict__.update(d)

    def parse_settings_dict(self, d):
        self.__dict__.update(d)
