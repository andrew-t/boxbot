# -*- coding:utf-8 -*-
import logging
from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw

from more_fonts import largest_font_that_fits

logging.basicConfig(level=logging.DEBUG)

# We use the screen on its side so swap these to avoid having to think about that elsewhere
width = epd2in13_V4.EPD_HEIGHT
height = epd2in13_V4.EPD_WIDTH

class Screen:
    def __enter__(self):
        logging.info("epd2in13_V4 Demo")
        self.epd = epd2in13_V4.EPD()
        logging.info("init and Clear")
        self.epd.init()
        self.epd.Clear(0xFF)
        return self

    def write(self, text):
        text_image = Image.new('1', (self.epd.height, self.epd.width), 255)
        text_draw = ImageDraw.Draw(text_image)
        self.epd.displayPartBaseImage(self.epd.getbuffer(text_image))
        text_draw.rectangle((120, 80, 220, 105), fill = 255)
        font, wrapped = largest_font_that_fits(text)
        text_draw.text((0, 10), wrapped, font=font, fill=0)
        text_image = text_image.rotate(180.0)
        self.epd.displayPartial(self.epd.getbuffer(text_image))

    def __exit__(self, exc_type, exc_value, traceback):
        epd2in13_V4.epdconfig.module_exit(cleanup=True)
