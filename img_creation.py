#!/usr/bin/python
from random import randint
from PIL import Image, ImageDraw, ImageFont
from collections import deque
from string import ascii_lowercase as chars_lower

'''
Need to consider changing of how YOLO splits the image
into 7x7 sections. Since we know initially we will
only want a single word highlighted by the user. This
should remove the need for a vertical split. 1x9?
Make the split a function of the length of pixels?

How to make a unreplicatable Test Set?
'''

# Want to randomize orientation of char (between 0-30 degress)
# Want to randomize image resolutions between (Note4 - S8)
# Want to randomize density of chars (Thin, Bold, Medium)
# Want to randomize italics, and none italics
# Want to randomize top 20 publishing Fonts
# Want to randomize top 5 publishing font sizes
# Want to randmoize obsfucation/noise between some reasonable range

# Best way to achieve lighting condtions?
## Want to mimic lighting conditions (range between white and red, saturation)?
## Want different degrees of background white (mimic lighting)?

# Want bash script to download all the necessary fonts

# Output 26 chars
# --> No word contains numbers
# Always white background
# Can download TTF files from https://fonts.google.com

## Randomize number of chars in image
## Supercalifragilisticexpialidocious
rnd_size = randint(1, 34)
chars = deque(maxlen=rnd_size)

## Randomize shade of black
## 90 arbitrary number
rnd_shade = randint(0, 90)
rnd_red = rnd_shade + randint(0, 2)
rnd_blue = rnd_shade + randint(0, 2)
rnd_green = rnd_shade + randint(0, 2)
rnd_alpha = rnd_shade + randint(0, 2)

rnd_black = (rnd_red, rnd_blue, rnd_green, rnd_alpha)

## Randomize chars
for i in range(0, rnd_size):
    rnd = randint(0, 25)
    c = chars_lower[rnd]
    chars.append(c)

# Initially user will highlight single word
# so only need single word per image
word = "".join(chars)

#for font in fonts:
for i in [0]:
    font = ImageFont.truetype("/Users/robbyrao/Downloads/Roboto/Roboto-Black.ttf", size=15)

# font size need to change in relation to image size
# word should be randomly moved x+0.5, y+0.5 from the center
# of the image

img = Image.new('RGBA', (200, 100), 'white')
draw = ImageDraw.Draw(img, "RGBA")
draw.text((20, 70), word, rnd_black, font=font)

img.save("imgname.jpg", "JPEG", dpi=(600, 600))
