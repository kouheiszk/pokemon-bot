#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum
import logging

from modules.item import items

log = logging.getLogger("pokemon_bot")


class Fort(object):
    def __init__(self, d):
        self.__dict__.update(d)
        self.fort_search = None

    def set_fort_search_dict(self, fort_search_dict):
        self.fort_search = FortSearch(fort_search_dict)

    def __str__(self):
        s = "\n# ポケストップ\n"
        s += "## 名前: {}\n".format(self.name)
        if self.fort_search is not None:
            if self.fort_search.result.is_success:
                s += "## スピンの経験値: {}\n".format(self.fort_search.experience_awarded)
                s += "## チェイン: {}\n".format(self.fort_search.chain_hack_sequence_number)
                s += "## スピンで得たアイテム:\n"
                for item_awarded in self.fort_search.items_awarded:
                    s += "- {}: {}個\n".format(items[item_awarded["item_id"]], item_awarded["item_count"])
            else:
                s += "## スピン: {}\n".format(self.fort_search.result)
        return s


class FortSearch(object):
    def __init__(self, d):
        self.__dict__.update(d)
        self.result = FortSearchResult(d.get("result", 0))


class FortSearchResult(enum.Enum):
    NO_RESULT_SET = 0
    SUCCESS = 1
    OUT_OF_RANGE = 2
    IN_COOLDOWN_PERIOD = 3
    INVENTORY_FULL = 4

    @property
    def is_success(self):
        return self.value == 1

    def __str__(self):
        return ["不明",
                "成功",
                "範囲外...",
                "時間をおいて...",
                "アイテムポーチがいっぱい"][self.value]
