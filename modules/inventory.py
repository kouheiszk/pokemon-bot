#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from modules.egg import Egg
from modules.incubator import Incubator
from modules.item import items
from modules.pokedex import pokedex
from modules.pokemon import Pokemon
from modules.stats import Stats

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
        self.stats = Stats()
        self.party = []
        self.eggs = []
        self.bag = {}

    @property
    def unused_incubators(self):
        filtered_incubators = filter(lambda i: i.pokemon_id == 0, self.incubators)
        return [i for i in filtered_incubators]

    def parse_response_dic(self, response_dict):
        self._dict = response_dict
        if bool(self._dict):
            log.debug("Response dictionary (get_inventory): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

        for item in self._dict.get("inventory_items", []):
            if item.get("inventory_item_data"):
                data = item.get("inventory_item_data")

                if data.get("player_stats"):
                    stats_dict = data.get("player_stats")
                    self.stats.parse_from_dict(stats_dict)
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
                        self.eggs.append(Egg(pokemon_data))
                    else:
                        self.party.append(Pokemon(pokemon_data))
                    continue

                incubators = data.get("egg_incubators", None)
                if incubators:
                    for incubator in incubators.get("egg_incubator", []):
                        self.incubators.append(Incubator(incubator))
                    continue

                bag_item = data.get("item", None)
                if bag_item:
                    self.bag[bag_item.get("item_id")] = bag_item.get("count", 0)
                    continue

    def __getattr__(self, attr):
        return self._dict.get(attr)

    def __str__(self):
        s = "\n# ステータス:\n"

        s += "## プレイヤーの状況:\n"
        s += "-- レベル {}\n".format(self.stats.level)
        s += "-- 経験値 {}/{}\n".format(self.stats.experience, self.stats.next_level_xp)
        s += "-- ポケモン捕獲状況 {}/{}\n".format(self.stats.pokemons_captured, self.stats.pokemons_encountered)

        s += "## パーティー:\n"
        for pokemon in self.party:
            s += "-- {0} cp:{1}\n".format(pokedex[pokemon.pokemon_id], pokemon.cp)

        s += "## たまご:\n"
        for egg in self.eggs:
            if egg.egg_incubator_id:
                s += "-- {0}km in:{1}\n".format(egg.egg_km_walked_target - egg.egg_km_walked_start,
                                                egg.egg_incubator_id)
            else:
                s += "-- {0}km\n".format(egg.egg_km_walked_target)

        s += "## バッグ:\n"
        for key in self.bag:
            s += "-- {0}: {1}\n".format(items[key], self.bag[key])

        s += "## 孵化器:\n"
        for incubator in self.incubators:
            remaining = incubator.uses_remaining
            if remaining:
                s += "-- {0} あと{1}回\n".format(incubator.id, remaining)
            else:
                s += "-- {0} 無限孵化器\n".format(incubator.id, remaining)
                
        return s
