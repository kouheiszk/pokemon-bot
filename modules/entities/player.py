#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum
import logging

from modules.utilities import time2str

log = logging.getLogger("pokemon_bot")


class Player(object):
    team = 0

    def __init__(self, d={}):
        self.__dict__.update(d)

    def parse_response_dic(self, d):
        self.__dict__.update(d)

    def __str__(self):
        s = "\n# プレイヤー\n"

        s += "## ユーザ名: {}\n".format(self.username)
        s += "## チーム: {}\n".format(Team(self.team).to_jp)
        for currency in self.currencies:
            s += "## {}: {}\n".format(currency.get("name"), currency.get("amount", 0))
        s += "## 作成日時: {}\n".format(time2str(self.creation_timestamp_ms))
        return s


class Team(enum.Enum):
    NONE = 0
    YELLOW = 1
    BLUE = 2
    RED = 3

    @property
    def to_jp(self):
        teams = ["未所属",
                 "黄チーム",
                 "青チーム",
                 "赤チーム"]
        return teams[self.value]

    def __str__(self):
        return self.to_jp
