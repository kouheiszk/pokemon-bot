#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.catch import Catch
from modules.entities.badges import Badges
from modules.entities.hatched_eggs import HatchedEggs
from modules.entities.inventory import Inventory
from modules.entities.map_objects import MapObjects
from modules.entities.player import Player
from modules.entities.settings import Settings


class State(object):
    def __init__(self):
        self.player = Player()
        self.inventory = Inventory()
        self.badges = Badges()
        self.settings = Settings()
        self.map_objects = MapObjects()
        self.catch = Catch()
        self.hatched_eggs = HatchedEggs(self.inventory)
