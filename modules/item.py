#!/usr/bin/python
# -*- coding: utf-8 -*-
import enum


class Item(enum.Enum):
    # Static Lookups
    UNKNOWN = 0
    POKE_BALL = 1
    GREAT_BALL = 2
    ULTRA_BALL = 3
    MASTER_BALL = 4
    POTION = 101
    SUPER_POTION = 102
    HYPER_POTION = 103
    MAX_POTION = 104
    REVIVE = 201
    MAX_REVIVE = 202
    LUCKY_EGG = 301
    INCENSE_ORDINARY = 401
    INCENSE_SPICY = 402
    INCENSE_COOL = 403
    INCENSE_FLORAL = 404
    TROY_DISK = 501
    X_ATTACK = 602
    X_DEFENSE = 603
    X_MIRACLE = 604
    RAZZ_BERRY = 701
    BLUK_BERRY = 702
    NANAB_BERRY = 703
    WEPAR_BERRY = 704
    PINAP_BERRY = 705
    SPECIAL_CAMERA = 801
    INCUBATOR_BASIC_UNLIMITED = 901
    INCUBATOR_BASIC = 902
    POKEMON_STORAGE_UPGRADE = 1001
    ITEM_STORAGE_UPGRADE = 1002

    def __str__(self):
        if self.value == 1:
            return "モンスターボール"
        elif self.value == 2:
            return "スーパーボール"
        elif self.value == 3:
            return "ハイパーボール"
        elif self.value == 4:
            return "マスターボール"
        elif self.value == 101:
            return "キズぐすり"
        elif self.value == 102:
            return "いいキズぐすり"
        elif self.value == 103:
            return "すごいキズぐすり"
        elif self.value == 104:
            return "まんたんのくすり"
        elif self.value == 201:
            return "げんきのかけら"
        elif self.value == 202:
            return "げんきのかたまり"
        elif self.value == 301:
            return "しあわせタマゴ"
        elif self.value == 401:
            return "おこう"
        elif self.value == 402:
            return "INCENSE_SPICY"
        elif self.value == 403:
            return "INCENSE_COOL"
        elif self.value == 404:
            return "INCENSE_FLORAL"
        elif self.value == 501:
            return "TROY_DISK"
        elif self.value == 602:
            return "X_ATTACK"
        elif self.value == 603:
            return "X_DEFENSE"
        elif self.value == 604:
            return "X_MIRACLE"
        elif self.value == 701:
            return "ズリのみ"
        elif self.value == 702:
            return "BLUK_BERRY"
        elif self.value == 703:
            return "NANAB_BERRY"
        elif self.value == 704:
            return "WEPAR_BERRY"
        elif self.value == 705:
            return "PINAP_BERRY"
        elif self.value == 801:
            return "カメラ"
        elif self.value == 901:
            return "ムゲンふかそうち"
        elif self.value == 902:
            return "ふかそうち"
        elif self.value == 1001:
            return "POKEMON_STORAGE_UPGRADE"
        elif self.value == 1002:
            return "ITEM_STORAGE_UPGRADE"
        else:
            return "不明"
