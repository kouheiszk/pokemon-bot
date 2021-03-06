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
from modules.bot import Bot

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
    logging.getLogger("pgoapi").setLevel(logging.WARNING)
    logging.getLogger("rpc_api").setLevel(logging.WARNING)
    logging.getLogger("pokemon_bot").setLevel(logging.INFO)

    # コンフィグ情報を元に各ライブラリのログレベルを調整
    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)
        logging.getLogger("pokemon_bot").setLevel(logging.DEBUG)

    session = Session(config.auth_service, config.username, config.password, config.location)
    if not session:
        raise GeneralPokemonBotException("Session not created successfully")

    bot = Bot(session)
    bot.get_profile()

    cooldown = 10  # sec

    # Run the bot
    while True:
        bot.check_inventory()
        map_objects = session.get_map_objects(both_direction=False)
        bot.clean_pokemon()
        bot.clean_inventory()

        try:
            bot.walk_and_catch_and_spin(map_objects)
            cooldown = 10

        # Catch problems and reauthenticate
        except GeneralPokemonBotException as e:
            log.critical('GeneralPokemonBotException raised: {0} \n {1}'.format(e, traceback.format_exc()))
            # 再認証したほうがいいかも？
            time.sleep(cooldown)
            cooldown *= 2

            # except Exception as e:
            #     log.critical('Exception raised: : {0} \n {1}'.format(e, traceback.format_exc()))
            #     # 再認証したほうがいいかも？
            #     time.sleep(cooldown)
            #     cooldown *= 2


if __name__ == "__main__":
    main()
