#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import textwrap
import traceback

from pygrister.api import GristApi
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Demo")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    font18 = ImageFont.truetype('RobotoMono.ttf', 18)
    font20 = ImageFont.truetype('RobotoMono.ttf', 20)
    font24 = ImageFont.truetype('RobotoMono.ttf', 24)

    load_dotenv()
    grist = GristApi()
    status_code, response = grist.list_records('BoxBot_Entries')
    entries = [entry['A'] for entry in response]
    print(entries)

    teststring = entries[0]
    wrapstring = "\n".join(textwrap.wrap(teststring, width=22))
    
    # # partial update
    logging.info("4.show text...")
    epd.init()
    text_image = Image.new('1', (epd.height, epd.width), 255)
    text_draw = ImageDraw.Draw(text_image)
    epd.displayPartBaseImage(epd.getbuffer(text_image))
    num = 0
    while (True):
        text_draw.rectangle((120, 80, 220, 105), fill = 255)
        text_draw.text((0, -5), wrapstring, font = font18, fill = 0)
        epd.displayPartial(epd.getbuffer(text_image))
        num = num + 1
        if(num == 20):
            break
    
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
