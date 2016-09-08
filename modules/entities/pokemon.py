#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from datetime import datetime

from modules.pokedex import Pokedex

log = logging.getLogger("pokemon_bot")


class Pokemon(object):
    def __init__(self, d):
        self.id = d.get("id", None)
        self.pokemon_id = d.get("pokemon_id", d.get("pokemon_data", {}).get("pokemon_id"))
        self.pokedex = Pokedex(self.pokemon_id)
        self.stamina = d.get("stamina", 0)
        self.individual_stamina = d.get("individual_stamina", 0)
        self.individual_defense = d.get("individual_defense", 0)
        self.individual_attack = d.get("individual_attack", 0)
        self.weight_kg = d.get("weight_kg", 0)
        self.height_m = d.get("height_m", 0)

        last_modified_timestamp_ms = d.get("last_modified_timestamp_ms", None)
        time_till_hidden_ms = d.get("time_till_hidden_ms", None)
        if last_modified_timestamp_ms and time_till_hidden_ms:
            self.disappear_time = datetime.utcfromtimestamp(
                (last_modified_timestamp_ms + time_till_hidden_ms) / 1000.0)
        else:
            self.disappear_time = None

        expiration_timestamp_ms = d.get("expiration_timestamp_ms", None)
        if expiration_timestamp_ms:
            self.expiration_time = datetime.utcfromtimestamp(expiration_timestamp_ms / 1000.0)
        else:
            self.expiration_time = None

        self._dict = d

    @property
    def is_weak(self):
        return self.individual_stamina < 10 or self.individual_defense < 10 or self.individual_attack < 10

    @property
    def is_evelvable(self):
        return self.pokedex.evolves is not None

    @property
    def max_cp(self):
        return self.pokedex.max_cp

    @property
    def name(self):
        return "{}".format(self.pokedex)

    def __getattr__(self, attr):
        return self._dict.get(attr)
