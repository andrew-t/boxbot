#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import textwrap
import traceback
import random
import datetime
import time as goto
from pygrister.api import GristApi
from dotenv import load_dotenv

from collections import namedtuple
SizedFont = namedtuple('SizedFont', ['font', 'line_length', 'max_lines'])

def get_text():
    status_code, response = grist.list_records('BoxBot_Entries')
    entries = [entry['A'] for entry in response]
    # print(entries)
    logging.info(f"Found {len(entries)} entries")
    entries = [entry for entry in entries if len(textwrap.wrap(entry, width=22))<6]
    logging.info(f"Found {len(entries)} entries after filtering")
    now = datetime.datetime.now()
    seed = int(str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute - (now.minute % 5)))
    random.seed(seed)
    entry = random.choice(entries)
    logging.info(f"Chose: {entry}")
    return entry

def update_screen():
    text = get_text()
    text_image = Image.new('1', (epd.height, epd.width), 255)
    text_draw = ImageDraw.Draw(text_image)
    epd.displayPartBaseImage(epd.getbuffer(text_image))
    text_draw.rectangle((120, 80, 220, 105), fill = 255)
    font, wrapped = largest_font_that_fits(text)
    text_draw.text((0, 10), wrapped, font=font, fill=0)
    text_image = text_image.rotate(180.0)
    epd.displayPartial(epd.getbuffer(text_image))

def largest_font_that_fits(text):
    for font in fonts:
        wrapped = textwrap.wrap(text, width=font.line_length)
        if len(wrapped) <= font.max_lines:
            logging.info(f"Chose font: {font}")
    else:
        # If the loop fails, log a warning, but continue to return the smallest font we have
        logging.warning("Failed to find a font small enough")
    return font.font, "\n".join(wrapped)

logging.basicConfig(level=logging.DEBUG)

def load_font(size):
    font = SizedFont(
        ImageFont.truetype('RobotoMono.ttf', size),
        line_length=int(400 / size),
        max_lines=int(90 / size)
    )
    logging.info(f"Loaded font at size {size}. Text area is {font.line_length} × {font.max_lines}")
    return font

try:
    logging.info("epd2in13_V4 Demo")
    load_dotenv()
    grist = GristApi()

    fonts = [ load_font(size) for size in [30, 24, 20, 18] ]

    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    logging.info('Starting main loop')
    while True:
        try:
            logging.info('Updating screen')
            update_screen()
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

finally:
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
