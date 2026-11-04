# -*- coding:utf-8 -*-
import logging
import random
import datetime
import time as goto
from dotenv import load_dotenv
from interval import Interval
from pygrister.api import GristApi

from base_font import text_fits_on_screen
import threading

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
grist = GristApi()

entries = ['No facts loaded yet']

try:
    with open("facts", "w") as f:
        entries = [ line for line in f.readlines() if line ]
except Exception as e:
    print("Couldn't load cached facts")

def load_entries():
    global entries
    try:
        status_code, response = grist.list_records('BoxBot_Entries')
        if status_code >= 400:
        	raise Exception(f'Failed with error code {status_code}')
        all_entries = [entry['A'] for entry in response]
        # print(entries)
        logging.info(f"Found {len(all_entries)} entries")
        entries = [entry for entry in all_entries if text_fits_on_screen(entry)]
        logging.info(f"Found {len(entries)} entries after filtering")
        if f:
        	with open("facts", "w") as f:
            	f.write('\n'.join(entries))
    except Exception as e:
        logging.error("Error loading entries", e)
        if not entries:
            entries = [str(e)]

load_entries()
interval = Interval(load_entries, 15*60)

def get_text():
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
