import textwrap
import math


def wrapline(text, font, maxwidth):
    text_length = len(text)
    font_length = font.size(text)[0]

    avg_char_len = math.floor(font_length / text_length) + 10

    wrap_len = math.floor(maxwidth / avg_char_len)

    wrapper = textwrap.TextWrapper()
    wrapper.replace_white_space = False
    wrapper.width = wrap_len

    return wrapper.wrap(text)


