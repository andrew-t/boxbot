# -*- coding:utf-8 -*-
import logging
from PIL import ImageFont
import textwrap

logging.basicConfig(level=logging.DEBUG)

FONT_SIZES = [36, 30, 24, 20, 18]

class SizedFont:
    def __init__(self, size):
        self.size = size
        self.font = ImageFont.truetype('RobotoMono.ttf', size)
        # Ideally we'd work these numbers out from font metrics and the screen size, but this works just fine:
        self.line_length = int(400 / size)
        self.max_lines = int(90 / size)
        logging.info(f"Loaded font at size {size}. Text area is {self.line_length} × {self.max_lines}")

    def wrap_text_if_fits(self, text):
        wrapped = textwrap.wrap(text, width=self.line_length)
        if len(wrapped) > self.max_lines:
            return False
        return wrapped

fonts = [ SizedFont(size) for size in FONT_SIZES ]
smallest_font = fonts[-1]

def text_fits_on_screen(text):
    return smallest_font.wrap_text_if_fits(text) is not False

def largest_font_that_fits(text):
    for font in fonts:
        wrapped = font.wrap_text_if_fits(text)
        if wrapped:
            logging.info(f"Chose font: {font.size}")
            break
    else:
        # If the loop fails, log a warning, but continue to return the smallest font we have
        logging.warning("Failed to find a font small enough")
    return font.font, "\n".join(wrapped)
