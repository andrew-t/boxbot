# -*- coding:utf-8 -*-
import logging
from PIL import ImageFont
import textwrap

logging.basicConfig(level=logging.DEBUG)

class BaseFont:
    def __init__(self):
        self.name = 'Roboto Mono 18'
        self.font = ImageFont.truetype('RobotoMono.ttf', 18)
        logging.info("Loaded RobotoMono.ttf at size 18")

    def wrap_text_if_fits(self, text):
        wrapped = textwrap.wrap(text, width=22)
        if len(wrapped) > 5:
            return False
        return wrapped

smallest_font = BaseFont()

def text_fits_on_screen(text):
    return smallest_font.wrap_text_if_fits(text) is not False
