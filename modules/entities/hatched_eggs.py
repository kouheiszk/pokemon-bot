#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class HatchedEggs(object):
    def __init__(self, d={}):
        self.__dict__.update(d)

    def parse_eggs_dict(self, d):
        self.__dict__.update(d)
        if len(d) >= 2:
            log.info("#####################################")
            log.info(d)
            log.info("#####################################")
