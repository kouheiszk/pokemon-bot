#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import time

from modules.route import Route

log = logging.getLogger("pokemon_bot")


class Bot(object):
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session

    @property
    def location(self):
        return self._session.location

    # プロフィール取得
    def get_profile(self):
        profile = self.session.get_profile()
        log.info(profile)

    # アイテムポーチの中をチェック
    def check_inventory(self):
        log.info(self.session.inventory)

    # cp以下のポケモンを博士に送る
    def clean_pokemon(self):
        self.session.clean_pokemon()

    # 持ちすぎているアイテムを捨てる
    def clean_inventory(self):
        self.session.clean_inventory()

    # 卵を孵化器に入れる
    def set_eggs_if_needed(self):
        self.session.set_eggs()

    def get_level_up_rewards_if_needed(self):
        self.session.get_level_up_rewards()

    def walk_and_catch_and_spin(self, map_objects, limit=10):
        sorted_pokestops = map_objects.sort_close_pokestops()
        pokestops = sorted_pokestops[:limit]
        pokestop_routes = Route.create_routes(pokestops)

        for num, pokestop_route in enumerate(pokestop_routes):
            map_objects = self.session.get_map_objects(both_direction=False)
            log.info("\n# ステップ: {}/{}".format(num + 1, len(pokestop_routes)))
            log.info(map_objects)

            # 歩き始める前にたまごを孵化器に入れる
            self.set_eggs_if_needed()

            # レベルアップリワードを受け取る
            self.get_level_up_rewards_if_needed()

            # 捕獲可能なポケモンを捕まえる
            catchable_pokemon_routes = Route.create_routes(map_objects.catchable_pokemons)
            for catchable_pokemon_route in catchable_pokemon_routes:
                self.session.walk_and_catch(catchable_pokemon_route, catch_on_way=False)

            # ポケストップへ行く
            self.session.walk_and_spin(pokestop_route)
            time.sleep(10)
