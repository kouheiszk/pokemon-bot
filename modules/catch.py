#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint
import random

import time

import sys

from modules.exceptions import GeneralPokemonBotException
from modules.item import items

log = logging.getLogger("pokemon_bot")


class Catch(object):
    def __init__(self):
        self.catches = []

    def is_catched_pokemon(self, pokemon):
        pokemon_encounter_ids = [p.encounter_id for p in self.catches]
        return bool(pokemon.encounter_id in pokemon_encounter_ids)
