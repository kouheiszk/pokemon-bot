#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.badges import Badges
from modules.catch import Catch
from modules.eggs import Eggs
from modules.inventory import Inventory
from modules.map_objects import MapObjects
from modules.player import Player
from modules.settings import Settings


class State(object):
    def __init__(self):
        self.player = Player()
        self.eggs = Eggs()
        self.inventory = Inventory()
        self.badges = Badges()
        self.settings = Settings()
        self.map_objects = MapObjects()
        # self.fortSearch = FortSearch()
        # self.fortDetails = FortDetails()
        # self.encounter = Encounter()
        self.catch = Catch()
        # self.itemCapture = ItemCapture()
        # self.itemPotion = ItemPotion()
        # self.itemRevive = ItemRevive()
        # self.evolve = Evolve()
        # self.release = Release()
        # self.recycle = Recycle()
        # self.incubator = EggIncubator()
        # self.nickname = Nickname()
        # self.playerTeam = PlayerTeam()
        # self.favoritePokemon = FavoritePokemon()
        # self.upgradePokemon = UpgradePokemon()
