#!/usr/bin/python
from random import randint
from PIL import Image, ImageDraw, ImageFont
from collections import deque
from string import ascii_lowercase as chars_lower

# Want to randomize location of char
# Want to randomize orientation of char (between 0-45 degress)
# Want to randomize image resolutions between (Note4 - S8)
# Want to randomize density of chars (Thin, Bold, Medium)
# Want to randomize italics, and none italics
# Want to randomize top 20 publishing Fonts
# Want to randomize top 5 publishing font sizes
# Want to randmoize obsfucation/noise between some reasonable range

# Output 26 chars
# --> No word contains numbers

# Always white background

# Can download TTF files from https://fonts.google.com

## Randomize number of chars in image
rand_size = randint(0, 9)
chars = deque(maxlen=rand_size)

"""
Traceback (most recent call last):
      File "img_creation.py", line 31, in <module>
          c = chars_lower[rnd]
          IndexError: string index out of range
"""

## Randomize chars
for i in range(0, rand_size):
    rnd = randint(0, 26)
    c = chars_lower[rnd]
    chars.append(c)

words = "".join(chars)

img = Image.new('RGB', (200, 100))
draw = ImageDraw.Draw(img, "RGBA")
# draw.text((x,y), "text to display", font=ImageFont.truetype(path, fontsize, encoding))
draw.text((20, 70), words, font=ImageFont.truetype("/Users/robbyrao/Downloads/Roboto/Roboto-Black.ttf", size=15))

img.save("imgname.jpg", "JPEG")
