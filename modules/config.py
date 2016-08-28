#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import getpass
import json
import logging
import os

from modules.exceptions import GeneralPokemonBotException

log = logging.getLogger("pokemon_bot")
user = "kouhei"


class Config(object):
    def __init__(self, config_file="config.json"):
        parser = argparse.ArgumentParser()

        # If config file exists, load variables from json
        load = {}
        if os.path.isfile(config_file):
            with open(config_file) as data:
                load.update(json.load(data)[user])

        # Read passed in Arguments
        required = lambda x: not x in load
        parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
                            required=required("auth_service"))
        parser.add_argument("-u", "--username", help="Username", required=required("username"))
        parser.add_argument("-p", "--password", help="Password")
        parser.add_argument("-l", "--location", help="Location", required=required("location"))
        parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
        parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
        parser.set_defaults(DEBUG=False, TEST=False)
        config = parser.parse_args()

        # Passed in arguments shoud trump
        for key in config.__dict__:
            if key in load and config.__dict__[key] is None:
                config.__dict__[key] = str(load[key])

        if config.__dict__["password"] is None:
            log.info("Secure Password Input (if there is no password prompt, use --password <pw>):")
            config.__dict__["password"] = getpass.getpass()

        if config.auth_service not in ['ptc', 'google']:
            raise GeneralPokemonBotException("Invalid Auth service specified! ('ptc' or 'google')")

        self.__dict__.update(config.__dict__)


config = Config()
