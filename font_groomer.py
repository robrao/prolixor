#!/usr/bin/python
import os
import fnmatch

from random import randint, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from collections import deque
from string import ascii_lowercase as chars_lower
from string import ascii_uppercase as chars_upper
from skimage.util import random_noise
from random import uniform as rnd_uniform

import numpy as np

def remove_fonts(font_paths):
    f = open("removed_fonts.txt", "w")

    for fp in font_paths:
        try:
            os.remove(fp)
            f.write(os.path.basename(fp))
            print "removed {}".format(fp)
        except OSError:
            print "couldn't find font: {}".format(fp)

    f.close()

if __name__ == "__main__":
    fonts = []
    # MacOS
    # for root, dirnames, filenames in os.walk('./fonts/fonts-master/'):
        # for filename in fnmatch.filter(filenames, '*.ttf'):
            # fonts.append(os.path.join(root, filename))
    # LinuxOS
    for ffile in os.listdir('/home/rrao/.fonts'):
        if ".ttf" in ffile:
            fonts.append(os.path.join('/home/rrao/.fonts', ffile))

    removed_font_paths = []
    for font_path in fonts:
        font_size = 100
        char_lower = []
        char_upper = []

        char_lower.append(chars_lower[0])
        char_upper.append(chars_upper[0])

        # Initially user will highlight single word
        # so only need single word per image
        c_lower = "".join(char_lower)
        c_upper = "".join(char_upper)

        font = ImageFont.truetype(font_path, size=font_size)

        # Image size changes in relation to font size
        im_w_f = font_size * 1
        im_h_f = font_size + im_w_f
        im_w = int(im_w_f)
        im_h = int(im_h_f)

        # randomize background on image
        img = Image.new('RGBA', (im_w, im_h), 'white')
        draw = ImageDraw.Draw(img, "RGBA")
        dw, dh = draw.textsize(c_lower, font)
        img2 = Image.new('RGBA', (im_w, im_h), 'white')
        draw2 = ImageDraw.Draw(img2, "RGBA")
        dw, dh = draw2.textsize(c_upper, font)

        cent_w = (im_w - dw) / 2.0
        cent_h = (im_h - dh) / 2.0
        x_jitter = randint(0, int((im_w - dw) * 0.25)) * choice([-1, 1])
        y_jitter = randint(0, int((im_h - dh) * 0.25)) * choice([-1, 1])
        txtx = cent_w + x_jitter
        txty = cent_h + y_jitter

        draw.text((txtx, txty), c_lower, (0, 0, 0, 0), font=font)
        draw2.text((txtx, txty), c_upper, (0, 0, 0, 0), font=font)

        #TODO: display images so they are not overlapped
        img.show()
        img2.show()

        del_or_no = raw_input('Delete this font? [y/N]');

        if del_or_no == 'y':
            removed_fonts_paths.append(font_path)
            print "{} as been queued for removal".format(os.path.basename(font_path))

        #TODO: Images are not being closed
        img.close()
        img2.close()

    #remove_fonts(removed_font_paths)
