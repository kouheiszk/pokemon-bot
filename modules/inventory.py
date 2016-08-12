#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from modules.item import items
from modules.pokedex import pokedex

log = logging.getLogger("pokemon_bot")


class Inventory(object):
    def __init__(self, initial_dict=None):
        self._dict = {}

        if initial_dict is None:
            initial_dict = {}
        self.parse_response_dic(initial_dict)

        self.incubators = []
        self.pokedex = {}
        self.candies = {}
        self.stats = {}
        self.party = []
        self.eggs = []
        self.bag = {}

    def parse_response_dic(self, response_dict):
        self._dict = response_dict.get("responses", {}).get("GET_INVENTORY", {}).get("inventory_delta", {})
        if bool(self._dict):
            log.debug("Response dictionary (get_inventory): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

        for item in self._dict.get("inventory_items", []):
            if item.get("inventory_item_data"):
                data = item.get("inventory_item_data")

                if data.get("player_stats"):
                    self.stats = data.get("player_stats")
                    continue

                pokedex_entry = data.get("pokedex_entry", None)
                if pokedex_entry:
                    self.pokedex[pokedex_entry.get("pokemon_id")] = pokedex_entry
                    continue

                candy = data.get("candy", None)
                if candy:
                    self.candies[candy.get("family_id")] = candy.get("candy")
                    continue

                pokemon_data = data.get("pokemon_data", None)
                if pokemon_data:
                    if pokemon_data.get('is_egg', False):
                        self.eggs.append(pokemon_data)
                    else:
                        self.party.append(pokemon_data)
                    continue

                incubators = data.get("egg_incubators", None)
                if incubators:
                    self.incubators = incubators.get("egg_incubator")
                    continue

                bag_item = data.get("item", None)
                if bag_item:
                    self.bag[bag_item.get("item_id")] = bag_item.get("count", 0)
                    continue

    def __getattr__(self, attr):
        return self._dict.get(attr)

    def __str__(self):
        s = "Inventory:\n"

        s += "-- Player Stats:\n"
        for key in self.stats:
            s += "\t{0}: {1}\n".format(key, self.stats[key])

        s += "-- Pokedex:\n"
        for key in self.pokedex:
            s += "\t{0}: {1}/{2}\n".format(pokedex[key],
                                           self.pokedex[key].get("times_captured"),
                                           self.pokedex[key].get("times_encountered"))

        s += "-- Candies:\n"
        for key in self.candies:
            s += "\t{0}: {1}\n".format(pokedex[key], self.candies[key])

        s += "-- Party:\n"
        for pokemon in self.party:
            s += "\t{0} cp:{1}\n".format(pokedex[pokemon.get("pokemon_id")], pokemon.get("cp"))

        s += "-- Eggs:\n"
        for egg in self.eggs:
            incubator_id = egg.get("egg_incubator_id", None)
            if incubator_id:
                s += "\t{0}km in:{1}\n".format(egg.get("egg_km_walked_target"), incubator_id)
            else:
                s += "\t{0}km\n".format(egg.get("egg_km_walked_target"))

        s += "-- Bag:\n"
        for key in self.bag:
            s += "\t{0}: {1}\n".format(items[key], self.bag[key])

        s += "-- Incubators:\n"
        for incubator in self.incubators:
            remaining = incubator.get("uses_remaining", None)
            if remaining:
                s += "\t{0} remaining:{1}\n".format(incubator.get("id"), remaining)
            else:
                s += "\t{0} mugen\n".format(incubator.get("id"), remaining)

        return s
