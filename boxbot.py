#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time as goto

from get_text import get_text, wait_until_next_update
from screen import Screen

logging.basicConfig(level=logging.DEBUG)

with Screen() as screen:
    try:
        logging.info('Starting main loop')
        while True:
            try:
                logging.info('Updating screen')
                text = get_text()
                screen.write(text)
                wait_until_next_update()
            except Exception as e:
                logging.warning('Failed to update screen')
                logging.warning(e)
                screen.write(str(e))
                goto.sleep(60)

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
