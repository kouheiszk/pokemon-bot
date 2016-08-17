#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger("pokemon_bot")


class Fort(object):
    def __init__(self, d):
        self.__dict__.update(d)
