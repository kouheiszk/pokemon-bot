#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from datetime import datetime

from modules.pokedex import pokedex

log = logging.getLogger("pokemon_bot")


class Pokemon(object):
    def __init__(self, p_dict=None):
        self.id = p_dict.get("id", None)
        self.pokemon_id = p_dict.get("pokemon_id", p_dict.get("pokemon_data", {}).get("pokemon_id"))
        self.rarity = pokedex.get_rarity_by_id(p_dict.get("pokemon_id"))
        self.stamina = p_dict.get("stamina", 0)
        self.individual_stamina = p_dict.get("individual_stamina", 0)
        self.individual_defense = p_dict.get("individual_defense", 0)
        self.individual_attack = p_dict.get("individual_attack", 0)
        self.weight_kg = p_dict.get("weight_kg", 0)
        self.height_m = p_dict.get("height_m", 0)
        self._dict = {}

        if p_dict is None:
            p_dict = {}
        self.parse_dic(p_dict)

    def parse_dic(self, p_dict):

        last_modified_timestamp_ms = p_dict.get("last_modified_timestamp_ms", None)
        time_till_hidden_ms = p_dict.get("time_till_hidden_ms", None)
        if last_modified_timestamp_ms and time_till_hidden_ms:
            p_dict["disappear_time"] = datetime.utcfromtimestamp(
                (last_modified_timestamp_ms + time_till_hidden_ms) / 1000.0)
        else:
            p_dict["disappear_time"] = None

        expiration_timestamp_ms = p_dict.get("expiration_timestamp_ms", None)
        if expiration_timestamp_ms:
            p_dict["expiration_time"] = datetime.utcfromtimestamp(expiration_timestamp_ms / 1000.0)
        else:
            p_dict["expiration_time"] = None

        self._dict = p_dict
        if bool(self._dict):
            log.debug("p_dict (pokemon): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

    def __getattr__(self, attr):
        return self._dict.get(attr)
