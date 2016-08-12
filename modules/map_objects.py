#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint

from datetime import datetime, timedelta

from modules.pokedex import pokedex

log = logging.getLogger("pokemon_bot")


class MapObjects(object):
    def __init__(self, initial_dict=None):
        self._dict = {}
        self.wild_pokemons = {}
        self.catchable_pokemons = {}
        self.pokestops = {}
        self.gyms = {}

        if initial_dict is None:
            initial_dict = {}
        self.parse_response_dic(initial_dict)

    def parse_response_dic(self, response_dict):
        wild_pokemons = {}
        catchable_pokemons = {}
        pokestops = {}
        gyms = {}

        self._dict = response_dict.get("responses", {}).get("GET_MAP_OBJECTS", {})
        if bool(self._dict):
            log.debug("Response dictionary (get_map_objects): \n\r{}"
                      .format(pprint.PrettyPrinter(indent=4).pformat(self._dict)))

            for cell in self.cells():
                for wp in cell.get("wild_pokemons", []):
                    wp["pokemon_id"] = wp.get("pokemon_id", wp.get("pokemon_data", {}).get("pokemon_id"))
                    wp["disappear_time"] = datetime.utcfromtimestamp(
                        (wp["last_modified_timestamp_ms"] + wp["time_till_hidden_ms"]) / 1000.0)
                    wp["rarity"] = pokedex.get_rarity_by_id(wp["pokemon_id"])

                    wild_pokemons[wp['encounter_id']] = wp

                for cp in cell.get("catchable_pokemons", []):
                    cp["pokemon_id"] = cp.get("pokemon_id", cp.get("pokemon_data", {}).get("pokemon_id"))
                    cp["expiration_time"] = datetime.utcfromtimestamp(
                        (cp["expiration_timestamp_ms"]) / 1000.0)
                    cp["rarity"] = pokedex.get_rarity_by_id(wp["pokemon_id"])

                    catchable_pokemons[cp['encounter_id']] = cp

                for f in cell.get("forts", []):
                    if f.get("type") == 1:  # ポケストップ
                        pokestop = f

                        if "active_fort_modifier" in f:
                            lure_expiration = datetime.utcfromtimestamp(
                                f["last_modified_timestamp_ms"] / 1000.0) + timedelta(minutes=30)
                            active_fort_modifier = f["active_fort_modifier"]
                        else:
                            lure_expiration, active_fort_modifier = None, None

                        pokestop["pokestop_id"] = f["id"]
                        pokestop["lure_expiration"] = lure_expiration
                        pokestop["active_fort_modifier"] = active_fort_modifier
                        pokestop["last_modified"] = datetime.utcfromtimestamp(
                            f["last_modified_timestamp_ms"] / 1000.0)

                        pokestops[f["id"]] = pokestop

                    elif f.get("type") is None:  # ジム
                        gym = f
                        gym["gym_id"] = f["id"]
                        gym["team_id"] = f.get("owned_by_team", 0)
                        gym["guard_pokemon_id"] = f.get("guard_pokemon_id", 0)
                        gym["gym_points"] = f.get("gym_points", 0)
                        gym["last_modified"] = datetime.utcfromtimestamp(
                            f["last_modified_timestamp_ms"] / 1000.0)

                        gyms[f["id"]] = gym

        self.wild_pokemons = wild_pokemons
        self.catchable_pokemons = catchable_pokemons
        self.pokestops = pokestops
        self.gyms = gyms

    def cells(self):
        return self._dict.get("map_cells", [])

    def __getattr__(self, attr):
        return self._dict.get(attr)

    def __str__(self):
        s = "MapObjects:\n"

        s += "-- Wild Pokemons:\n"
        for key in self.wild_pokemons:
            pokemon = self.wild_pokemons[key]
            s += "\t{0}: {1}\n".format(pokedex[pokemon["pokemon_id"]], pokemon)

        s += "-- Catchable Pokemons:\n"
        for key in self.catchable_pokemons:
            pokemon = self.catchable_pokemons[key]
            s += "\t{0}: {1}\n".format(pokedex[pokemon["pokemon_id"]], pokemon)

        s += "-- Pokestops:\n"
        s += "\t{0} stops\n".format(len(self.pokestops))

        s += "-- Gyms:\n"
        s += "\t{0} gyms\n".format(len(self.gyms))

        return s
