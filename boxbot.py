#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time as goto

from get_text import get_text
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
                logging.info('Waiting for next update')
                goto.sleep(300)
            except Exception as e:
                logging.warning('Failed to update screen')
                logging.warning(e)
                goto.sleep(60)

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
