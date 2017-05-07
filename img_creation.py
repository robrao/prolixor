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
-> set different rand seed for Test and Train?

Image must have max height and width. With in
which we can move the text, which can be a varying
size.
-> we can determine max height and width by using
google translates box as an example.
x-> This can cause issues because there may be an
letter from another word that still remains in
the image
x-> how would you know once the word has been
correctly selected?
|
--> allow user to highlight word.
--> will need a max height
--> assuming largest font used in print is 20points
--> set max height for highlight box from that max font size
--> max width of image can be set from max phone screen width
x--> hightlighting box can also have additional chars being selected
---> solve later...possibly lstms, or simple clustering of chars based
on centeriod.

*-> the image size trained on should be a function of:
    * font size
    * number of characters
Image size does not matter because the data distribution we are trying
to imitate is the characters not the image. The changing of the image
size based off the font size will add sufficient randomization for images
anyway.

Recalculate anchor boxes using ground truth.
'''

# Want to randomize orientation of char (between 0-30 degress)
# Want to randomize image resolutions between (Note4 - S8)
# Want to randomize density of chars (Thin, Bold, Medium)
# Want to randomize italics, and none italics
# Want to randomize top 20 publishing Fonts
# Want to randomize top 5 publishing font sizes
# Want to randmoize obsfucation/noise between some reasonable range
# Want to output label (char) and x, y, w, h of bbx (x, y, being center of bbx?)
# Want to randomly add random degree of blur to image

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

font_size = randint(10, 150)
for i in [0]:
    font = ImageFont.truetype("/Users/robbyrao/Downloads/Roboto/Roboto-Black.ttf", size=font_size)

# font size need to change in relation to image size
# word should be randomly moved x+0.5, y+0.5 from the center
# of the image
#im_w = int(font_size * rnd_size * 0.61) # c/im_w = 0.6052
#im_h = int(font_size + 10) # c/im_w = 0.7105
im_w = int(font_size * rnd_size) # c/im_w = 0.6052
im_h = int(font_size) # c/im_w = 0.7105

print "font size: {}".format(font_size)
print "# of chars: {}".format(rnd_size)
print "im wxh: {} {}".format(im_w, im_h)
print "word: {}".format(word)

img = Image.new('RGBA', (im_w, im_h), 'white') #randomize background
draw = ImageDraw.Draw(img, "RGBA")
draw.line((img.size[0]/2.0, 0) + (img.size[0]/2.0, img.size[1]), fill=128)
draw.line((0, img.size[1]/2.0, img.size[0], img.size[1]/2.0), fill=128)
dw, dh = draw.textsize(word)
cent_w = (im_w/2.0) - dw # rounding issues?
cent_h = (im_h/2.0) - dh # rounding issues?

print "word wxh: {} {}".format(dw, dh)
print "cent wxh: {} {}".format(cent_w, cent_h)

draw.text((cent_w, cent_h), word, rnd_black, font=font)

img.save("imgname.jpg", "JPEG", dpi=(600, 600))
