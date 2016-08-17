#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Catch(object):
    def __init__(self):
        self._catches = []

    def is_catchable_pokemon(self, pokemon):
        pokemon_encounter_ids = [p.encounter_id for p in self._catches]
        return bool(pokemon.encounter_id not in pokemon_encounter_ids)

    def start_catching(self, pokemon):
        self._catches.append(pokemon)
