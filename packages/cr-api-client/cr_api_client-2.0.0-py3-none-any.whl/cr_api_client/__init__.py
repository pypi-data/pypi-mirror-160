#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Component version
__version__ = "2.0.0"

import sys

from loguru import logger


# Initialize loguru
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "|<level>{level: ^7}</level>| {message}",
        },
    ],
}
logger.configure(**config)
