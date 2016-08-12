#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import time

import sys
from distutils.version import StrictVersion

from modules.api import Api
from modules.config import config

# Currently supported pgoapi
pgoapi_version = "1.1.7"

log = logging.getLogger(__name__)

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


def main():
    # ログフォーマットの設定
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')

    # 各ライブラリのログレベルを調整
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    logging.getLogger("rpc_api").setLevel(logging.INFO)

    # コンフィグ情報を元に各ライブラリのログレベルを調整
    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    api = Api(config.location)
    api.authenticate(config.auth_service, config.username, config.password)

    log.debug("################# 10s ####################")
    time.sleep(10)

    inventory = api.get_inventory()
    log.debug(inventory)

    while True:
        log.debug("################# 10s ####################")
        time.sleep(10)
        map_objects = api.get_map_objects()
        log.debug(map_objects)
        return


if __name__ == "__main__":
    main()
