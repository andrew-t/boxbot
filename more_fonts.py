# -*- coding:utf-8 -*-
import logging
from PIL import ImageFont

from base_font import smallest_font
import screen

logging.basicConfig(level=logging.DEBUG)

FONT_SIZES = [36, 30, 24, 20]

class SizedFont:
    def __init__(self, size):
        self.name = f"Roboto Regular {size}px"
        self.font = ImageFont.truetype('Roboto.ttf', size)
        logging.info(f"Loaded Roboto Regular at size {size}")

    def wrap_text_if_fits(self, text):
        lines = []
        current_line = ''
        max_width = 0

        for word in text.split(' '):
            if not word: continue
            if word == '/':
                lines.append(current_line)
                current_line = ''
                continue
            current_line_with_word = f"{current_line} {word}".strip()
            width = self.font.getlength(current_line_with_word)
            if width > screen.width:
                lines.append(current_line)
                current_line = word
                continue
            if width > max_width: max_width = width
            current_line = current_line_with_word
        lines.append(current_line)
        lines = [line for line in lines if line]

        left, top, width, line_height = self.font.getbbox('M')
        total_height = len(lines) * line_height
        # assume a 20px margin top and bottom
        if total_height > screen.height - 20:
            logging.debug(f"Rejected font {self.name} with wrapping")
            for line in lines:
                logging.debug(f"-- {line}")
            logging.debug(f"Size is {max_width}×{total_height} for a {screen.width}×{screen.height} screen")
            return False
        logging.info(f"Chose font: {self.name}")
        logging.debug(f"Size is {max_width}×{total_height} for a {screen.width}×{screen.height} screen")
        return lines

fonts = [
    *(SizedFont(size) for size in FONT_SIZES),
    smallest_font
]

def largest_font_that_fits(text):
    for font in fonts:
        wrapped = font.wrap_text_if_fits(text)
        if wrapped: break
    else:
        # If the loop fails, log a warning, but continue to return the smallest font we have
        logging.warning("Failed to find a font small enough")
    return font.font, "\n".join(wrapped)
