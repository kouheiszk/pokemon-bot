#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum
import logging

from modules.entities.pokemon import Pokemon

log = logging.getLogger("pokemon_bot")


class Evolve(object):
    def __init__(self, base_pokemon, d):
        self.__dict__.update(d)
        self.base_pokemon = base_pokemon
        self.pokemon = Pokemon(d.get("evolved_pokemon_data", {}))
        self.status = EvolveResult(d.get("result", 0))

    def __str__(self):
        s = "\n# 進化\n"
        s += "## ポケモン: {} -> {}\n".format(self.base_pokemon.name, self.pokemon.name)
        s += "## ステータス: {}\n".format(self.status)
        if self.status.is_success:
            s += "## 経験値: +{}XP\n".format(self.experience_awarded)
            s += "## {}のアメ: +{}\n".format(self.base_pokemon.name, self.candy_awarded)

        return s


class EvolveResult(enum.Enum):
    UNSET = 0
    SUCCESS = 1
    FAILED_POKEMON_MISSING = 2
    FAILED_INSUFFICIENT_RESOURCES = 3
    FAILED_POKEMON_CANNOT_EVOLVE = 4
    FAILED_POKEMON_IS_DEPLOYED = 5

    @property
    def is_success(self):
        return self.value == 1

    def __str__(self):
        return ["UNKNOWN",
                "成功",
                "進化するポケモンが不明",
                "アメが足りない",
                "進化できなかった",
                "ジムに配置されているぞ！"][self.value]
