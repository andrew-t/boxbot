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


def get_text():
    status_code, response = grist.list_records('BoxBot_Entries')
    entries = [entry['A'] for entry in response]
    # print(entries)
    entries = [textwrap.wrap(entry,width=22) for entry in entries]
    entries = [entry for entry in entries if len(entry)<6]
    now = datetime.datetime.now()
    seednumber = int(str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute - (now.minute % 5)))
    random.seed(seednumber)
    entry = random.choice(entries)
    return entry

def update_screen():        
    textstring = get_text()
    wrapstring = "\n".join(textstring)
    text_image = Image.new('1', (epd.height, epd.width), 255)
    text_draw = ImageDraw.Draw(text_image)
    epd.displayPartBaseImage(epd.getbuffer(text_image))
    text_draw.rectangle((120, 80, 220, 105), fill = 255)
    text_draw.text((0, 10), wrapstring, font = font18, fill = 0)
    text_image = text_image.rotate(180.0)
    epd.displayPartial(epd.getbuffer(text_image))

logging.basicConfig(level=logging.DEBUG)
    
try:
    logging.info("epd2in13_V4 Demo")
    load_dotenv()
    grist = GristApi()
    
    font18 = ImageFont.truetype('RobotoMono.ttf', 18)
    font20 = ImageFont.truetype('RobotoMono.ttf', 20)
    font24 = ImageFont.truetype('RobotoMono.ttf', 24)

    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    logging.info('here1')
    while True:
        try:
            logging.info('here2')
            update_screen()
            logging.info('here3')
            goto.sleep(300)
        except:
            goto.sleep(60)
            
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
