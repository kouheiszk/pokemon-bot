#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class HatchedEggs(object):
    def __init__(self, inventory):
        self._inventory = inventory
        self.eggs = []

    def parse_eggs_dict(self, d):
        pokemon_ids = d.get("pokemon_id", [])
        for index, pokemon_id in enumerate(pokemon_ids):
            stardust = d.get("stardust_awarded", [0] * len(pokemon_ids))[index]
            experience = d.get("experience_awarded", [0] * len(pokemon_ids))[index]
            candy = d.get("candy_awarded", [0] * len(pokemon_ids))[index]
            self.eggs.append(HatchedEgg(pokemon_id, stardust, experience, candy))

    def __str__(self):
        s = "\n# ふかしたたまご\n"
        if self.eggs:
            while self.eggs:
                egg = self.eggs.pop()
                pokemon = self._inventory.party[egg.pokemon_id]
                s += "## ポケモン: {}\n".format(pokemon.name)
                s += "- 経験値: +{}\n".format(egg.experience)
                s += "- ほしのすな: +{}\n".format(egg.stardust)
                s += "- あめ: +{}\n".format(egg.candy)
        else:
            s += "- なし\n"

        return s


class HatchedEgg(object):
    def __init__(self, pokemon_id, stardust, experience, candy):
        self.pokemon_id = pokemon_id
        self.stardust = stardust
        self.experience = experience
        self.candy = candy
