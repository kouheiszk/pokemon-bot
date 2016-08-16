#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import time

import sys
import traceback
from distutils.version import StrictVersion

from modules.config import config

from modules.exceptions import GeneralPokemonBotException
from modules.session import Session

log = logging.getLogger("pokemon_bot")

# Assert pgoapi is installed
try:
    import pgoapi
except ImportError:
    log.critical("It seems `pgoapi` is not installed. You must run pip install -r requirements.txt again")
    sys.exit(1)

if not hasattr(pgoapi, "__version__") or StrictVersion(pgoapi.__version__) < StrictVersion("1.1.7"):
    log.critical("It seems `pgoapi` is not up-to-date. You must run pip install -r requirements.txt again")
    sys.exit(1)


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

    session = Session(config.location)
    session.authenticate(config.auth_service, config.username, config.password)
    cooldown = 10  # sec

    # Run the bot
    while True:
        inventory = session.get_inventory()
        log.info(inventory)

        map_objects = session.get_map_objects()
        log.info(map_objects)

        # 不要な持ち物を削除
        session.clean_pokemon(threshold_cp=500)
        session.clean_inventory()

        sys.exit(0)

        try:
            # 捕まえることができるポケモンを捕まえる
            # TODO catchable_pokemons とか配列にする
            for pokemon in map_objects.catchable_pokemons:
                if walk_and_catch(api, pokemon, inventory):
                    map_objects.catched(catched_pokemons)
                    # 捕まえたポケモンを削除する
                    if encounter_id in map_objects.wild_pokemons:
                        del map_objects.wild_pokemons[encounter_id]

            # まだ捕まえていない野生のポケモンを捕まえる
            for pokemon in map_objects.wild_pokemons:
                walk_and_catch(api, pokemon)

            for pokestop in map_objects.pokestops:
                walk_and_spin(api, pokestop)

                # TODO 卵をチェックする

            sys.exit(0)

            cooldown = 10

        # Catch problems and reauthenticate
        except GeneralPokemonBotException as e:
            log.critical('GeneralPokemonBotException raised: {0} \n {1}'.format(e, traceback.format_exc()))
            # 再認証したほうがいいかも？
            time.sleep(cooldown)
            cooldown *= 2

        except Exception as e:
            log.critical('Exception raised: : {0} \n {1}'.format(e, traceback.format_exc()))
            # 再認証したほうがいいかも？
            time.sleep(cooldown)
            cooldown *= 2


if __name__ == "__main__":
    main()
