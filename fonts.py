# -*- coding:utf-8 -*-
import logging
from PIL import ImageFont
import textwrap

from collections import namedtuple
SizedFont = namedtuple('SizedFont', ['font', 'size', 'line_length', 'max_lines'])

FONT_SIZES = [30, 24, 20, 18]

def load_font(size):
    font = SizedFont(
        ImageFont.truetype('RobotoMono.ttf', size),
        size,
        # Ideally we'd work these numbers out from font metrics and the screen size, but this works just fine:
        line_length=int(400 / size),
        max_lines=int(90 / size)
    )
    logging.info(f"Loaded font at size {size}. Text area is {font.line_length} × {font.max_lines}")
    return font

fonts = [ load_font(size) for size in FONT_SIZES ]
smallest_font = fonts[-1]

def wrap_text_if_fits(text, font):
    wrapped = textwrap.wrap(text, width=font.line_length)
    if len(wrapped) > font.max_lines:
        return False
    return wrapped

def text_fits_on_screen(text):
    return wrap_text_if_fits(text, smallest_font) is not False

def largest_font_that_fits(text):
    for font in fonts:
        wrapped = wrap_text_if_fits(text, font)
        if wrapped:
            logging.info(f"Chose font: {font.size}")
            break
    else:
        # If the loop fails, log a warning, but continue to return the smallest font we have
        logging.warning("Failed to find a font small enough")
    return font.font, "\n".join(wrapped)
