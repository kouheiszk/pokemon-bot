#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from datetime import datetime, timedelta

log = logging.getLogger("pokemon_bot")


class Pokestop(object):
    def __init__(self, s_dict={}):
        self.id = s_dict.get("id", None)
        self.pokestop_id = s_dict.get("id", None)
        self.latitude = s_dict.get("latitude")
        self.longitude = s_dict.get("longitude")
        self.cooldown_complete_timestamp_ms = s_dict.get("cooldown_complete_timestamp_ms", 0)

        if "active_fort_modifier" in s_dict:
            self.lure_expiration = datetime.utcfromtimestamp(
                s_dict["last_modified_timestamp_ms"] / 1000.0) + timedelta(minutes=30)
            self.active_fort_modifier = s_dict["active_fort_modifier"]
        else:
            self.lure_expiration = None
            self.active_fort_modifier = None

        self.last_modified = datetime.utcfromtimestamp(
            s_dict["last_modified_timestamp_ms"] / 1000.0)

        self._dict = s_dict

    def __getattr__(self, attr):
        return self._dict.get(attr)
