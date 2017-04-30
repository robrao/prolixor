#!/usr/bin/python

from PIL import Image, ImageDraw, ImageFont

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


img = Image.new('RGB', (200, 100))
draw = ImageDraw.Draw(img, "RGBA")
# draw.text((x,y), "text to display", font=ImageFont.truetype(path, fontsize, encoding))
draw.text((20, 70), "Ada LoveLace", font=ImageFont.truetype("/Users/robbyrao/Downloads/Roboto/Roboto-Black.ttf", size=15))

img.save("imgname.jpg", "JPEG")
