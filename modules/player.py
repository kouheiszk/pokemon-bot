#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger("pokemon_bot")


class Player(object):
    def __init__(self, initial_dict=None):
        self._dict = {}

        if initial_dict is None:
            initial_dict = {}
        self.parse_response_dic(initial_dict)

    def parse_response_dic(self, response_dict):
        self._dict = response_dict.get("responses", {}).get("GET_PLAYER", {}).get("player_data", {})
        if bool(self._dict):
            log.debug("Response dictionary (get_player): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

    def __getattr__(self, attr):
        return self._dict.get(attr)
