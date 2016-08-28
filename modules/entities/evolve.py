#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Evolve(object):
    def __init__(self, pokemon, d):
        self.__dict__.update(d)
        self.pokemon = pokemon

    def __str__(self):
        s = "\n# 進化:\n"
        s += "## ポケモン: {}\n".format(self.pokemon.name)
        s += "## 経験値: +{}XP\n".format(self.experience_awarded)
        s += "## {}のアメ: +{}\n".format(self.pokemon.name, self.candy_awarded)
        return s
