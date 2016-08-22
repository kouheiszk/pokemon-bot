#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("pokemon_bot")


class Stats(object):
    def __init__(self):
        self.should_get_level_up_rewarded = False
        self._rewarded_level = None

    def parse_from_dict(self, stats_dict):
        self.__dict__.update(stats_dict)

        # レベルアップの報酬を受け取る
        level = stats_dict.get("level", 0)
        if self._rewarded_level is not None and level > self._rewarded_level:
            self.should_get_level_up_rewarded = True
        self._rewarded_level = level
