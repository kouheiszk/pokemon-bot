#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import platform

import sys

import time
from datetime import datetime

log = logging.getLogger("pokemon_bot")


# @see https://github.com/PokemonGoMap/PokemonGo-Map/blob/83fab06f4fea54a58d0b0cebb95bed24551037c7/pogom/utils.py#L302
def get_encryption_lib_path():
    # win32 doesn't mean necessarily 32 bits
    if sys.platform == "win32" or sys.platform == "cygwin":
        if platform.architecture()[0] == '64bit':
            lib_name = "encrypt64bit.dll"
        else:
            lib_name = "encrypt32bit.dll"

    elif sys.platform == "darwin":
        lib_name = "libencrypt-osx-64.so"

    elif os.uname()[4].startswith("arm") and platform.architecture()[0] == '32bit':
        lib_name = "libencrypt-linux-arm-32.so"

    elif os.uname()[4].startswith("aarch64") and platform.architecture()[0] == '64bit':
        lib_name = "libencrypt-linux-arm-64.so"

    elif sys.platform.startswith('linux'):
        if "centos" in platform.platform():
            if platform.architecture()[0] == '64bit':
                lib_name = "libencrypt-centos-x86-64.so"
            else:
                lib_name = "libencrypt-linux-x86-32.so"
        else:
            if platform.architecture()[0] == '64bit':
                lib_name = "libencrypt-linux-x86-64.so"
            else:
                lib_name = "libencrypt-linux-x86-32.so"

    elif sys.platform.startswith('freebsd'):
        lib_name = "libencrypt-freebsd-64.so"

    else:
        err = "Unexpected/unsupported platform '{}'".format(sys.platform)
        log.error(err)
        raise Exception(err)

    lib_path = os.path.join(os.path.dirname(__file__), "libencrypt", lib_name)

    if not os.path.isfile(lib_path):
        err = "Could not find {} encryption library {}".format(sys.platform, lib_path)
        log.error(err)
        raise Exception(err)

    return lib_path


def time2str(second, millisecond=True):
    if millisecond:
        second /= 1000
    return datetime(*time.localtime(second)[:5]).strftime("%Y/%m/%d %H:%M:%S")
