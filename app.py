#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import random

import time

import sys
from distutils.version import StrictVersion

from modules.api import Api
from modules.config import config

# Currently supported pgoapi
from modules.exceptions import GeneralPokemonBotException
from modules.item import items
from modules.pokedex import pokedex

pgoapi_version = "1.1.7"

log = logging.getLogger("pokemon_bot")

# Assert pgoapi is installed
try:
    import pgoapi
    from pgoapi import utilities as util
except ImportError:
    log.critical("It seems `pgoapi` is not installed. You must run pip install -r requirements.txt again")
    sys.exit(1)

# Assert pgoapi >= pgoapi_version
if not hasattr(pgoapi, "__version__") or StrictVersion(pgoapi.__version__) < StrictVersion(pgoapi_version):
    log.critical("It seems `pgoapi` is not up-to-date. You must run pip install -r requirements.txt again")
    sys.exit(1)


def clean_pokemon(api, threshold_cp=50, delay=5):
    logging.info("Cleaning out Pokemon...")
    evolables = [pokedex.PIDGEY, pokedex.RATTATA, pokedex.ZUBAT]
    to_evolve = {evolve: [] for evolve in evolables}
    for pokemon in api.inventory.party:
        # If low cp, throw away
        if pokemon.get("cp") < threshold_cp:
            # It makes more sense to evolve some,
            # than throw away
            if pokemon.get("pokemon_id") in evolables:
                to_evolve[pokemon.get("pokemon_id")].append(pokemon)
                continue

            # Get rid of low CP, low evolve value
            log.info("Releasing %s" % pokedex[pokemon.get("pokemon_id")])
            api.release_pokemon(pokemon)  # FIXME
            time.sleep(delay)

    # Evolve those we want
    for evolve in evolables:
        # if we don't have any candies of that type
        # e.g. not caught that pokemon yet
        if evolve not in api.inventory.candies:
            continue
        candies = api.inventory.candies[evolve]
        pokemons = to_evolve[evolve]
        # release for optimal candies
        while candies // pokedex.evolves[evolve] < len(pokemons):
            pokemon = pokemons.pop()
            log.info("Releasing %s" % pokedex[pokemon.get("pokemon_id")])
            api.release_pokemon(pokemon)
            time.sleep(delay)
            candies += 1

        # evolve remainder
        for pokemon in pokemons:
            log.info("Evolving %s" % pokedex[pokemon.get("pokemon_id")])
            log.info(api.evolve_pokemon(pokemon))  # FIXME
            time.sleep(delay)
            api.release_pokemon(pokemon)
            time.sleep(delay)


def clean_inventory(api, delay=5):
    logging.info("Cleaning out Inventory...")
    bag = api.inventory.bag

    # Clear out all of a crtain type
    tossable = [items.POTION, items.SUPER_POTION, items.REVIVE]
    for toss in tossable:
        if toss in bag and bag[toss]:
            api.recycle_item(toss, count=bag[toss])  # FIXME
            time.sleep(delay)

    # Limit a certain type
    limited = {
        items.POKE_BALL: 50,
        items.GREAT_BALL: 100,
        items.ULTRA_BALL: 150,
        items.RAZZ_BERRY: 25
    }
    for limit in limited:
        if limit in bag and bag[limit] > limited[limit]:
            api.recycle_item(limit, count=(bag[limit] - limited[limit]))
            time.sleep(delay)


def walk_and_catch(api, pokemon, delay=2):
    if pokemon:
        log.info("Catching %s:" % pokedex[pokemon.get("pokemon_id")])
        api.walk_to(pokemon.latitude, pokemon.longitude, step=3.2)
        time.sleep(delay)
        result = encounter_and_catch(api, pokemon)
        log.info(result)
        return result
    else:
        return None


def encounter_and_catch(api, pokemon, threshold_p=0.5, limit=5, delay=2):
    # Start encounter
    encounter = api.encounter_pokemon(pokemon)  # FIXME
    time.sleep(config.general_cooldown_time / 2)

    # If party full
    if encounter.status == encounter.POKEMON_INVENTORY_FULL:  # FIXME
        raise GeneralPokemonBotException("Can't catch! Party is full!")

    # Grab needed data from proto
    chances = encounter.capture_probability.capture_probability
    balls = encounter.capture_probability.pokeball_type
    balls = balls or [items.POKE_BALL, items.GREAT_BALL, items.ULTRA_BALL]
    bag = api.inventory.bag

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
                api.use_item_capture(items.RAZZ_BERRY, pokemon)  # FIXME
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
        attempt = api.catch_pokemon(pokemon, best_ball)  # FIXME
        time.sleep(delay)

        # Success or run away
        if attempt.status == 1:
            return attempt

        # CATCH_FLEE is bad news
        if attempt.status == 3:
            if count == 0:
                log.info("Possible soft ban.")
            else:
                log.info("Pokemon fled at %dth attempt" % (count + 1))
            return attempt

        # Only try up to x attempts
        count += 1
        if count >= limit:
            log.info("Over catch limit")
            return None


# Walk to fort and spin
def walk_and_spin(api, pokestop, delay=2):
    if pokestop:
        details = api.get_fort_details(pokestop)  # FIXME
        log.info("Spinning the Fort \"%s\":" % details.get("name"))
        time.sleep(delay)

        api.walk_to(pokestop.get("latitude"), pokestop.get("longitude"), step=3.2)  # FIXME
        time.sleep(delay)

        log.info(api.get_fort_search(pokestop))  # FIXME
        time.sleep(delay)


def set_egg(api):
    inventory = api.inventory

    # If no eggs, nothing we can do
    if len(inventory.eggs) == 0:
        return None

    egg = inventory.eggs[0]
    incubator = inventory.incubators[0]
    return api.set_egg(incubator, egg)  # FIXME


def run(api):
    cooldown = 10  # sec

    # Run the bot
    while True:
        inventory = api.get_inventory()
        log.info(inventory)
        time.sleep(config.general_cooldown_time)

        map_objects = api.get_map_objects()
        log.info(map_objects)
        time.sleep(config.general_cooldown_time)
        return

        # 不要な持ち物を削除
        clean_pokemon(api, threshold_cp=500)
        clean_inventory(api)

        try:
            # 捕まえることができるポケモンを捕まえる
            for pokemon in map_objects.catchable_pokemons:
                if walk_and_catch(api, pokemon):
                    # 捕まえたポケモンを削除する
                    encounter_id = pokemon.get("encounter_id")
                    if encounter_id in map_objects.wild_pokemons:
                        del map_objects.wild_pokemons[encounter_id]

            # まだ捕まえていない野生のポケモンを捕まえる
            for pokemon in map_objects.wild_pokemons:
                walk_and_catch(api, pokemon)

            for pokestop in map_objects.pokestops:
                walk_and_spin(api, pokestop)
                time.sleep(config.general_cooldown_time / 2)

            cooldown = 10

        # Catch problems and reauthenticate
        except GeneralPokemonBotException as e:
            log.critical('GeneralPokemonBotException raised: %s', e)
            # 再認証したほうがいいかも？
            time.sleep(cooldown)
            cooldown *= 2

        except Exception as e:
            log.critical('Exception raised: %s', e)
            # 再認証したほうがいいかも？
            time.sleep(cooldown)
            cooldown *= 2


def main():
    # ログフォーマットの設定
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')

    # 各ライブラリのログレベルを調整
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    logging.getLogger("rpc_api").setLevel(logging.INFO)
    logging.getLogger("pokemon_bot").setLevel(logging.INFO)

    # コンフィグ情報を元に各ライブラリのログレベルを調整
    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)
        logging.getLogger("pokemon_bot").setLevel(logging.DEBUG)

    api = Api(config.location)
    api.authenticate(config.auth_service, config.username, config.password)
    run(api)


if __name__ == "__main__":
    main()
