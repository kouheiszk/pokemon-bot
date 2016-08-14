#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

import datetime

from modules.pokedex import pokedex

log = logging.getLogger("pokemon_bot")


class Pokemon(object):
    def __init__(self, initial_dict=None):
        self._dict = {}

        if initial_dict is None:
            initial_dict = {}
        self.parse_dic(initial_dict)

    def parse_dic(self, dict):
        dict["id"] = dict.get("pokemon_id", dict.get("pokemon_data", {}).get("pokemon_id"))
        dict["rarity"] = pokedex.get_rarity_by_id(dict["pokemon_id"])

        last_modified_timestamp_ms = dict.get("last_modified_timestamp_ms", None)
        time_till_hidden_ms = dict.get("time_till_hidden_ms", None)
        if last_modified_timestamp_ms and time_till_hidden_ms:
            dict["disappear_time"] = datetime.utcfromtimestamp(
                (last_modified_timestamp_ms + time_till_hidden_ms) / 1000.0)
        else:
            dict["disappear_time"] = None

        expiration_timestamp_ms = dict.get("expiration_timestamp_ms", None)
        if expiration_timestamp_ms:
            dict["expiration_time"] = datetime.utcfromtimestamp(expiration_timestamp_ms / 1000.0)
        else:
            dict["expiration_time"] = None

        self._dict = dict
        if bool(self._dict):
            log.debug("Dictionary (pokemon): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

    def __getattr__(self, attr):
        return self._dict.get(attr)
