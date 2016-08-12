#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger("pokemon_bot")


class Badges(object):
    def __init__(self, initial_dict=None):
        self._dict = {}

        if initial_dict is None:
            initial_dict = {}
        self.parse_response_dic(initial_dict)

    def parse_response_dic(self, response_dict):
        self._dict = response_dict.get("responses", {}).get("CHECK_AWARDED_BADGES", {})
        if bool(self._dict):
            log.debug("Response dictionary (check_awarded_badges): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

    def __getattr__(self, attr):
        return self._dict.get(attr)
