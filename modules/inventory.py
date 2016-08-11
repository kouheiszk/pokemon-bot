#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

log = logging.getLogger(__name__)


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

                pokemon_family = data.get("pokemon_family", None)
                if pokemon_family:
                    self.candies[pokemon_family.get("family_id")] = pokemon_family.get("candy")
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
