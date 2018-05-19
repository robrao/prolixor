#!/usr/bin/python
import os
import fnmatch
import pandas as pd

from random import randint, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from collections import deque
from string import ascii_lowercase as chars_lower
from string import ascii_uppercase as chars_upper
from skimage.util import random_noise
from random import uniform as rnd_uniform

import numpy as np


def max_value_search(img, x_coord, y_coord, font_colour, width):
    x_previous = x_coord
    x_final = x_coord + width
    max_val = img.getpixel((x_coord, y_coord))
    background_value = img.getpixel((0, 0))

    while x_coord < x_final:
        current_pixel = img.getpixel((x_coord, y_coord))

        if current_pixel >= img.getpixel((x_previous, y_coord)):
            if current_pixel < background_value and current_pixel > font_colour:
                max_val = img.getpixel((x_coord, y_coord))

        x_previous = x_coord
        x_coord += 0.1

    return max_val


def pixel_search(img, x_coord, y_coord, height, img_height, max_val):
    y_initial = y_coord
    y_final = y_coord + height

    while y_coord < y_final and y_coord < img_height:
        if img.getpixel((x_coord, y_coord)) < max_val:  # does not match background values
            x_coord -= 0.1  # shift to the left
            y_coord = y_initial

        y_coord += 0.1

    return x_coord

if __name__ == "__main__":
    fonts = []
    # for root, dirnames, filenames in os.walk('./fonts/fonts-master/'):
        # for filename in fnmatch.filter(filenames, '*.ttf'):
            # fonts.append(os.path.join(root, filename))
    for ffile in os.listdir('/home/rrao/.fonts'):
        if ".ttf" in ffile:
            fonts.append(os.path.join('/home/rrao/.fonts', ffile))
    if (os.path.isfile('font_data.csv')):
        print "FOUND DATA FILE"
        font_data = pd.read_csv('font_data.csv', sep=',')
        print font_data['fonts']

    # for idx in range(0, 10):
    for idx in range(0, 1):
        font_size = randint(30, 150)

        # Randomize shade of black
        rnd_shade = randint(0, 90)
        rnd_red = rnd_shade + randint(0, 2)
        rnd_blue = rnd_shade + randint(0, 2)
        rnd_green = rnd_shade + randint(0, 2)
        rnd_alpha = rnd_shade + randint(0, 2)

        rnd_black = (rnd_red, rnd_blue, rnd_green, rnd_alpha)

        # Randomize chars
        # rnd = randint(0, 25)
        rnd = 9
        char = str(chars_lower[rnd])

        # Randomize fonts
        rand_int = randint(0, len(fonts))
        font_path = fonts[randint(0, len(fonts))]
        # font_path = "/home/rrao/.fonts/Signika-Light.ttf"
        font = ImageFont.truetype(font_path, size=font_size)

        # Image size changes in relation to font size
        im_w_f = font_size * 2
        im_h_f = font_size + im_w_f
        im_w = int(im_w_f)
        im_h = int(im_h_f)

        # randomize background on image
        img = Image.new('RGBA', (im_w, im_h), 'white')
        draw = ImageDraw.Draw(img, "RGBA")
        bbx = draw.textsize(char, font=font)

        # per char size
        # w, h = draw.textsize(c, font)
        # char_size = (w, h)
        # char_offset = font.getoffset(c)

        try:
            cent_w = (im_w - bbx[0]) / 2.0
            cent_h = (im_h - bbx[1]) / 2.0
            x_jitter = randint(0, int((im_w - bbx[0]) * 0.25)) * choice([-1, 1])
            y_jitter = randint(0, int((im_h - bbx[1]) * 0.25)) * choice([-1, 1])
            txtx = cent_w + x_jitter
            txty = cent_h + y_jitter
        except ValueError as e:
            print "Error: test bbx 0 > img width -- ignoring..."
            continue

        draw.text((txtx, txty), char, rnd_black, font=font)

        offset = [txtx, txty]

        x1 = offset[0] #+ charoffset_x
        y1 = offset[1] #+ charoffset_y

        max_val = max_value_search(img, x1, y1, rnd_black, bbx[0])
        x1 = pixel_search(img, x1, y1, bbx[1], im_h, max_val)

        x2 = x1 + bbx[0]
        y2 = offset[1] + bbx[1]

        w = bbx[0]/im_w_f
        h = bbx[1]/im_h_f
        cx = (x1 + 0.5 * bbx[0])/im_w_f
        cy = (y1 + 0.5 * bbx[1])/im_h_f

        draw.rectangle([x1, y1, x2, y2], outline='red')

        label = "font: {} char: {} - {} {} {} {}".format(font_path, rnd, cx, cy, w, h)
        print label

        # Blur image
        # rnd_blur = rnd_uniform(0.0, 20.0) * im_h_f/1000
        # img = img.filter(ImageFilter.GaussianBlur(rnd_blur))

        # Noise Image
        # npim = np.asarray(img)
        # noise = random_noise(
                # npim,
                # 'speckle',
                # mean=rnd_uniform(0, 2),
                # var=rnd_uniform(0.01, 0.1)
        # )
        # res = npim * noise
        # img = Image.fromarray(np.uint8(res))

        img.show()
        # img.save("imgname_{}.jpg".format(idx), "JPEG", dpi=(600, 600))
