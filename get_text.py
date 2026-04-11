# -*- coding:utf-8 -*-
import logging
import random
import datetime
import time as goto
from dotenv import load_dotenv
from pygrister.api import GristApi

from fonts import text_fits_on_screen

logging.basicConfig(level=logging.DEBUG)

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

def wait_until_next_update():
    now = datetime.datetime.now()
    # Add a second just to make sure we catch the *next* update rather than displaying this one again
    time = 301 - ((now.minute % 5) * 60 + now.second)
    logging.info(f'Waiting {time}s for next update')
    goto.sleep(time)
