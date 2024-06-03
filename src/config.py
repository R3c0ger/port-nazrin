#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/config.py
# https://thwiki.cc/%E5%A8%9C%E5%85%B9%E7%8E%B2

import qlogging
from colorama import Fore, Back, Style


TITLE = "PortNazrin"
VERSION = "0.1.0"

# log_level = "debug"
log_level = "info"
log_file = "PortNazrin.log"
log_file_mode = "w"
LOGGER = qlogging.get_logger(
    level=log_level,
    logfile=log_file,
    logfilemode=log_file_mode,
    # loggingmode='long',
    loggingmode='manual',
    format_str='%(color)s%(message)s%(reset)s',
    colors={
        "DEBUG": Fore.CYAN + Style.BRIGHT,
        "INFO": Fore.GREEN + Style.BRIGHT,
        "WARNING": Fore.YELLOW + Style.BRIGHT,
        "ERROR": Fore.RED + Style.BRIGHT,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    }
)
