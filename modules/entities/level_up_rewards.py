#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from modules.item import Item

log = logging.getLogger("pokemon_bot")


class LevelUpRewards(object):
    def __init__(self, level, d):
        self.level = level
        self.__dict__.update(d)

    def __str__(self):
        s = "\n# レベルアップ\n"
        s += "## レベル: {}\n".format(self.level)
        s += "## レベルアップ報酬:\n"
        if self.items_awarded:
            for item_awarded in self.items_awarded:
                s += "- {}: {}個\n".format(Item(item_awarded["item_id"]), item_awarded["item_count"])
        else:
            s += "- 無し\n"
        return s
