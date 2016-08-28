#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum
import logging

from modules.pokedex import Pokedex

log = logging.getLogger("pokemon_bot")


class Encounter(object):
    def __init__(self, pokemon, d):
        self.__dict__.update(d)
        self.pokemon = pokemon
        self.status = EncounterResult(self.status)
        self.attempt = None
        self.attempt_count = 1
        self.berried = False

    @property
    def capture_probability(self):
        return self.__dict__.get("capture_probability", {})

    def set_catch_pokemon_dict(self, catch_pokemon_dict):
        self.attempt = PokemonCatchAttempt(catch_pokemon_dict)

    def __str__(self):
        s = "\n# エンカウント\n"
        s += "## ポケモン: {}\n".format(self.pokemon.name)
        s += "## 試行回数: {}\n".format(self.attempt_count)
        s += "## ズリのみ: {}\n".format("使用" if self.berried else "未使用")
        s += "## 捕獲報酬:\n"
        if self.attempt.status.is_success:
            s += "- ほしのすな: +{}\n".format(sum(self.attempt.capture_award.get("stardust", [])))
            s += "- {}のあめ: +{}\n".format(self.pokemon.name, sum(self.attempt.capture_award.get("candy", [])))
            s += "- 経験値: +{}XP\n".format(sum(self.attempt.capture_award.get("xp", [])))
        else:
            s += "- {}\n".format(self.attempt.status)
        return s


class EncounterResult(enum.Enum):
    ERROR = 0
    SUCCESS = 1
    NOT_FOUND = 2
    CLOSED = 3
    POKEMON_FLED = 4
    NOT_IN_RANGE = 5
    ALREADY_HAPPENED = 6
    POKEMON_INVENTORY_FULL = 7

    @property
    def is_party_full(self):
        return self.value == 7


class PokemonCatchAttempt(object):
    def __init__(self, d):
        self.__dict__.update(d)
        self.status = PokemonCatchResult(self.status)


class PokemonCatchResult(enum.Enum):
    ERROR = 0
    SUCCESS = 1
    ESCAPE = 2
    FLEE = 3
    MISSED = 4

    @property
    def is_success(self):
        return self.value == 1

    @property
    def is_flee(self):
        return self.value == 3

    def __str__(self):
        return ["エラー",
                "成功",
                "逃げた",
                "飛んでいった",
                "失敗"][self.value]
