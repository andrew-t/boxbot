#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import random
import datetime
from dotenv import load_dotenv
from pygrister.api import GristApi

from fonts import text_fits_on_screen

load_dotenv()
grist = GristApi()

def get_text():
    status_code, response = grist.list_records('BoxBot_Entries')
    entries = [entry['A'] for entry in response]
    # print(entries)
    logging.info(f"Found {len(entries)} entries")
    entries = [entry for entry in entries if text_fits_on_screen(entry)]
    logging.info(f"Found {len(entries)} entries after filtering")
    now = datetime.datetime.now()
    seed = int(str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute - (now.minute % 5)))
    random.seed(seed)
    entry = random.choice(entries)
    logging.info(f"Chose: {entry}")
    return entry
