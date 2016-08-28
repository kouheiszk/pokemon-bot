#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger("pokemon_bot")


class Badges(object):
    def __init__(self, d={}):
        self.__dict__.update(d)

    def parse_badges_dict(self, d):
        self.__dict__.update(d)
