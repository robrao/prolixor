#!/usr/bin/python
import os
import fnmatch

from random import randint, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from collections import deque
from string import ascii_lowercase as chars_lower
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
    for root, dirnames, filenames in os.walk('./fonts/fonts-master/'):
        for filename in fnmatch.filter(filenames, '*.ttf'):
            fonts.append(os.path.join(root, filename))

    for idx in range(0, 10):
        # Randomize number of chars in image
        # Supercalifragilisticexpialidocious
        font_size = randint(30, 150)
        max_chars = int(34 * (1/(font_size/10.0)))
        num_chars = randint(1, max_chars)
        chars = deque(maxlen=num_chars)

        # Randomize shade of black
        # 90 arbitrary number
        rnd_shade = randint(0, 90)
        rnd_red = rnd_shade + randint(0, 2)
        rnd_blue = rnd_shade + randint(0, 2)
        rnd_green = rnd_shade + randint(0, 2)
        rnd_alpha = rnd_shade + randint(0, 2)

        rnd_black = (rnd_red, rnd_blue, rnd_green, rnd_alpha)

        # Randomize chars
        chars_num = []
        for i in range(0, num_chars):
            rnd = randint(0, 25)
            c = chars_lower[rnd]
            chars.append(c)
            chars_num.append(rnd)

        # Initially user will highlight single word
        # so only need single word per image
        word = "".join(chars)

        font_path = fonts[randint(0, len(fonts))]
        font = ImageFont.truetype(font_path, size=font_size)

        # Image size changes in relation to font size
        im_w_f = font_size * num_chars
        im_h_f = font_size + im_w_f
        im_w = int(im_w_f)
        im_h = int(im_h_f)

        # randomize background on image
        img = Image.new('RGBA', (im_w, im_h), 'white')
        draw = ImageDraw.Draw(img, "RGBA")
        dw, dh = draw.textsize(word, font)

        # per char size
        char_size = []
        char_offset = []
        for c in chars:
            w, h = draw.textsize(c, font)
            csize = (w, h)
            offset = font.getoffset(c)
            char_size.append(csize)
            char_offset.append(offset)

        cent_w = (im_w - dw) / 2.0
        cent_h = (im_h - dh) / 2.0
        x_jitter = randint(0, int((im_w - dw) * 0.25)) * choice([-1, 1])
        y_jitter = randint(0, int((im_h - dh) * 0.25)) * choice([-1, 1])
        txtx = cent_w + x_jitter
        txty = cent_h + y_jitter

        draw.text((txtx, txty), word, rnd_black, font=font)

        offset = [txtx, txty]
        labels = []
        for idx, bbx in enumerate(char_size):
            charoffset_x, charoffset_y = char_offset[idx]

            x1 = offset[0] + charoffset_x
            y1 = offset[1] + charoffset_y

            max_val = max_value_search(img, x1, y1, rnd_black, bbx[0])
            x1 = pixel_search(img, x1, y1, bbx[1], im_h, max_val)

            x2 = x1 + bbx[0]
            y2 = offset[1] + bbx[1]

            w = bbx[0]/im_w_f
            h = bbx[1]/im_h_f
            cx = (x1 + 0.5 * bbx[0])/im_w_f
            cy = (y1 + 0.5 * bbx[1])/im_h_f

            draw.rectangle([x1, y1, x2, y2], outline='red')

            label = "{} {} {} {} {}".format(chars_num[idx], cx, cy, w, h)

            labels.append(label)
            offset[0] = x2

        # Blur image
        rnd_blur = rnd_uniform(0.0, 20.0) * im_h_f/1000
        img = img.filter(ImageFilter.GaussianBlur(rnd_blur))

        # Noise Image
        npim = np.asarray(img)
        noise = random_noise(
                npim,
                'speckle',
                mean=rnd_uniform(0, 2),
                var=rnd_uniform(0.01, 0.1)
        )
        res = npim * noise
        img = Image.fromarray(np.uint8(res))

        img.show()
        # img.save("imgname_{}.jpg".format(idx), "JPEG", dpi=(600, 600))
