#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint
import time

from datetime import datetime

from modules.location import Location
from modules.pokedex import pokedex
from modules.pokemon import Pokemon
from modules.pokestop import Pokestop

log = logging.getLogger("pokemon_bot")


class MapObjects(object):
    def __init__(self, initial_dict=None):
        self._dict = {}
        self.wild_pokemons = []
        self.catchable_pokemons = []
        self.pokestops = []
        self.gyms = []

        if initial_dict is None:
            initial_dict = {}
        self.parse_response_dic(initial_dict)

    def parse_response_dic(self, response_dict):
        wild_pokemons = []
        catchable_pokemons = []
        pokestops = []
        gyms = []

        self._dict = response_dict
        if bool(self._dict):
            log.debug("Response dictionary (get_map_objects): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

            for cell in self.cells():
                for wp in cell.get("wild_pokemons", []):
                    wild_pokemons.append(Pokemon(wp))

                for cp in cell.get("catchable_pokemons", []):
                    catchable_pokemons.append(Pokemon(cp))

                for f in cell.get("forts", []):
                    if f.get("type") == 1:  # ポケストップ
                        pokestop = Pokestop(f)
                        pokestops.append(pokestop)

                    elif f.get("type") is None:  # ジム
                        gym = f
                        gym["gym_id"] = f["id"]
                        gym["team_id"] = f.get("owned_by_team", 0)
                        gym["guard_pokemon_id"] = f.get("guard_pokemon_id", 0)
                        gym["gym_points"] = f.get("gym_points", 0)
                        gym["last_modified"] = datetime.utcfromtimestamp(
                            f["last_modified_timestamp_ms"] / 1000.0)

                        gyms.append(gym)

        self.wild_pokemons = wild_pokemons
        self.catchable_pokemons = catchable_pokemons
        self.pokestops = pokestops
        self.gyms = gyms

    def cells(self):
        return self._dict.get("map_cells", [])

    def sort_close_pokestops(self):
        ordered_pokestops = []

        for pokestop in [p for p in self.pokestops if p.cooldown_complete_timestamp_ms < time.time()]:
            ordered_pokestops.append({
                'hilbert': Location.get_lat_long_index(
                    pokestop.latitude, pokestop.longitude
                ),
                'pokestop': pokestop
            })

        ordered_pokestops = sorted(ordered_pokestops, key=lambda p: p["hilbert"])
        return [p["pokestop"] for p in ordered_pokestops]

    def get_spinable_pokestops(self, latitude, longitude):
        spinable_pokestops = []
        for pokestop in [p for p in self.pokestops if p.cooldown_complete_timestamp_ms < time.time()]:
            distance = Location.get_distance(
                latitude,
                longitude,
                pokestop.latitude,
                pokestop.longitude
            )
            spinable_pokestops.append({
                'distane': distance,
                'pokestop': pokestop
            })

        # 15m以下のポケストップを返す
        return [p["pokestop"] for p in spinable_pokestops if p["distane"] < 15]

    def __getattr__(self, attr):
        return self._dict.get(attr)

    def __str__(self):
        s = "MapObjects:\n"

        s += "-- Wild Pokemons:\n"
        for pokemon in self.wild_pokemons:
            s += "\t{0}: {1}\n".format(pokedex[pokemon.pokemon_id], pokemon)

        s += "-- Catchable Pokemons:\n"
        for pokemon in self.catchable_pokemons:
            s += "\t{0}: {1}\n".format(pokedex[pokemon.pokemon_id], pokemon)

        s += "-- Pokestops:\n"
        s += "\t{0} stops\n".format(len(self.pokestops))

        s += "-- Gyms:\n"
        s += "\t{0} gyms\n".format(len(self.gyms))

        return s
