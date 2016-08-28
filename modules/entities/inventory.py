#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from modules.entities.egg import Egg
from modules.entities.incubator import Incubator
from modules.entities.pokemon import Pokemon
from modules.entities.stats import Stats
from modules.item import Item
from modules.pokedex import Pokedex

log = logging.getLogger("pokemon_bot")


class Inventory(object):
    def __init__(self, d=None):
        self._dict = {}

        if d is not None:
            self.parse_inventory_dict(d)

        self.stats = Stats()
        self.pokedex = {}
        self.candies = {}
        self.eggs = {}
        self.party = {}
        self.incubators = {}
        self.bag = {}

    @property
    def unused_incubators(self):
        filtered_incubators = filter(lambda i: i.pokemon_id is None, self.incubators.values())
        return [i for i in filtered_incubators]

    def parse_inventory_dict(self, response_dict):
        self._dict = response_dict
        if bool(self._dict):
            log.debug("Response dictionary (get_inventory): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

        for item in self._dict.get("inventory_items", []):
            if item.get("inventory_item_data"):
                data = item.get("inventory_item_data")

                if data.get("player_stats"):
                    stats_dict = data.get("player_stats")
                    self.stats.parse_stats_dict(stats_dict)
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
                        egg = Egg(pokemon_data)
                        self.eggs[egg.id] = egg
                    else:
                        pokemon = Pokemon(pokemon_data)
                        self.party[pokemon.id] = pokemon
                    continue

                incubators = data.get("egg_incubators", None)
                if incubators:
                    for incubator in incubators.get("egg_incubator", []):
                        incubator = Incubator(incubator)
                        self.incubators[incubator.id] = incubator
                    continue

                bag_item = data.get("item", None)
                if bag_item:
                    self.bag[bag_item.get("item_id")] = bag_item.get("count", 0)
                    continue

    def __getattr__(self, attr):
        return self._dict.get(attr)

    def __str__(self):
        s = "\n# ステータス\n"

        s += "## プレイヤーの状況:\n"
        s += "- レベル {}\n".format(self.stats.level)
        s += "- 経験値 {}/{}\n".format(self.stats.experience, self.stats.next_level_xp)
        s += "- ポケモン捕獲状況 {}/{}\n".format(self.stats.pokemons_captured, self.stats.pokemons_encountered)

        s += "## パーティー:\n"
        for _, pokemon in self.party.items():
            s += "- {} (CP:{}, ATK:{}, DFS:{}, STM:{})\n".format(Pokedex(pokemon.pokemon_id),
                                                                 pokemon.cp,
                                                                 pokemon.individual_attack,
                                                                 pokemon.individual_defense,
                                                                 pokemon.individual_stamina)

        s += "## たまご:\n"
        for _, egg in self.eggs.items():
            if egg.egg_incubator_id:
                s += "- {}km ({}の中)\n".format(egg.egg_km_walked_target - egg.egg_km_walked_start,
                                             self.incubators[egg.egg_incubator_id])
            else:
                s += "- {}km\n".format(egg.egg_km_walked_target)

        s += "## バッグ:\n"
        for key in self.bag:
            s += "- {}: {}\n".format(Item(key), self.bag[key])

        s += "## ふかそうち:\n"
        for _, incubator in self.incubators.items():
            s += "- {}\n".format(incubator)

        return s
