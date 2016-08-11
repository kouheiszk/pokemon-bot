#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from modules.api import Api
from modules.config import config

log = logging.getLogger(__name__)


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
    inventory = api.get_inventory()
    log.debug("#####################################")
    log.debug(inventory)


if __name__ == "__main__":
    main()
