#!/usr/bin/python
# -*- coding: utf-8 -*-
from modules.badges import Badges
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
