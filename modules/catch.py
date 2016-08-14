#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import pprint
import random

import time

import sys

from modules.exceptions import GeneralPokemonBotException
from modules.item import items

log = logging.getLogger("pokemon_bot")


class Catch(object):
    def __init__(self, api):
        self._api = api
        self.catches = []

    def encounter_and_catch(self, pokemon, inventory, threshold_p=0.5, limit=5, delay=2):
        if not self._is_catched_pokemon(pokemon):
            return None

        self.catches.append(pokemon)

        # Start encounter
        encounter = self._api._encounter_pokemon(pokemon)
        time.sleep(delay)

        # If party full
        if encounter.status == encounter.POKEMON_INVENTORY_FULL:
            raise GeneralPokemonBotException("Can't catch! Party is full!")

        # Grab needed data from proto
        chances = encounter.capture_probability.capture_probability
        balls = encounter.capture_probability.pokeball_type
        balls = balls or [items.POKE_BALL, items.GREAT_BALL, items.ULTRA_BALL]
        bag = inventory.bag

        # Have we used a razz berry yet?
        berried = False

        # Make sure we aren't oer limit
        count = 0

        # Attempt catch
        while True:
            best_ball = items.UNKNOWN
            alt_ball = items.UNKNOWN

            # Check for balls and see if we pass
            # wanted threshold
            print(balls)
            for i, ball in enumerate(balls):
                print(bag.get(ball, 0) > 0)
                if bag.get(ball, 0) > 0:
                    alt_ball = ball
                    if chances[i] > threshold_p:
                        best_ball = ball
                        break

            # If we can't determine a ball, try a berry
            # or use a lower class ball
            if best_ball == items.UNKNOWN:
                if not berried and bag.get(items.RAZZ_BERRY, 0) > 0:
                    logging.info("Using a RAZZ_BERRY")
                    self._api.use_item_capture(items.RAZZ_BERRY, pokemon)
                    berried = True
                    time.sleep(delay + random.randint(1, 3))
                    continue

                # if no alt ball, there are no balls
                elif alt_ball == items.UNKNOWN:
                    raise GeneralPokemonBotException("Out of usable balls")
                else:
                    best_ball = alt_ball

            # Try to catch it!!
            log.info("Using a %s" % items[best_ball])
            attempt = self._api.catch_pokemon(pokemon, best_ball)
            time.sleep(delay)

            # Success or run away
            if attempt.status == 1:
                return attempt

            # CATCH_FLEE is bad news
            if attempt.status == 3:
                if count == 0:
                    log.info("Possible soft ban.")
                else:
                    log.info("Pokemon fled at {}th attempt".format(count + 1))
                return attempt

            # Only try up to x attempts
            count += 1
            if count >= limit:
                log.info("Over catch limit")
                return None

    def _is_catched_pokemon(self, pokemon):
        pokemon_encounter_ids = [p.encounter_id for p in self.catches]
        return bool(pokemon.encounter_id in pokemon_encounter_ids)
