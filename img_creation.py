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

def pixel_search(img, x_coord, y_coord, height, max_val):
    # if the number of pixels crossed less than the max value increase in that direction stop
    # searching in that direction, and return without entering a value in to the incident list
    # incident list will be a list of tuples: (x_coord, # of incidents)
    # therefore the last number in the list will be the one with lowest incidents, and min
    # movement in that direction

    # first value in both lists will be the initial tuple
    left_incidents = []
    right_incidents = []
    anchor = x_coord
    y_initial = y_coord
    y_final = y_coord + height
    continue_search = True

    while continue_search:
        incident_count = 0

        while y_coord < y_final:
            if img.getpixel((x_coord, y_coord)) < max_val:  # does not match background values
                incident_count += 1

                if len(left_incidents) > 1 \
                        and left_incidents[-1] < incident_count:
                    continue_search = False
                    break

            y_coord += 0.1

        if continue_search:
            left_incidents.append((x_coord, incident_count))
            x_coord -= 0.1  # shift to the left
            y_coord = y_initial

        if left_incidents[-1][1] == 0:
            break

    # reset
    x_left = x_coord
    x_coord = anchor
    y_coord = y_initial
    continue_search = True

    while continue_search:
        incident_count = 0

        while y_coord < y_final:
            if img.getpixel((x_coord, y_coord)) < max_val:  # does not match background values
                incident_count += 1

                if len(right_incidents) > 1 \
                       and right_incidents[-1] < incident_count:
                    continue_search = False
                    break

            y_coord += 0.1

        if continue_search:
            right_incidents.append((x_coord, incident_count))
            x_coord += 0.1  # shift to the right
            y_coord = y_initial

        if right_incidents[-1][1] == 0:
            break

    print "left incidents: {}".format(left_incidents[-1])
    print "right incidents: {}".format(right_incidents[-1])

    # import pudb;pu.db

    # need new/more robust comparison method
    left_coord, lincidents = left_incidents[-1]
    right_coord, rincidents = right_incidents[-1]
    left_score = abs(anchor - left_coord)**2 + lincidents**2
    right_score = abs(anchor - right_coord)**2 + rincidents**2

    if left_score < right_score:
        x_coord = left_coord
    else:
        x_coord = right_coord

    return x_coord

if __name__ == "__main__":
    fonts = []
    for root, dirnames, filenames in os.walk('./fonts/fonts-master/'):
        for filename in fnmatch.filter(filenames, '*.ttf'):
            fonts.append(os.path.join(root, filename))
    
    for count, font_path in enumerate([fonts[0]]):
        font_size = 55
        num_chars = 26
        chars = deque(maxlen=num_chars)
        rnd_black = (0,0,0,0)
    
        chars_num = []
        for i in range(0, num_chars):
            c = chars_lower[i]
            chars.append(c)
    
        word = "".join(chars)
    
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
    
        cent_w_img = (im_w - dw) / 2.0
        cent_h_img = (im_h - dh) / 2.0
        x_jitter = 0
        y_jitter = 0
        x_txt = cent_w_img + x_jitter
        y_txt = cent_h_img + y_jitter
    
        draw.text((x_txt, y_txt), word, rnd_black, font=font)
    
        offset = [x_txt, y_txt]
        bbxs = []
        for idx, bbx in enumerate(char_size):
            charoffset_x, charoffset_y = char_offset[idx]
            x1 = offset[0] + charoffset_x
            y1 = offset[1] + charoffset_y

            # if idx > 22:
                # import pudb;pu.db

            max_val = max_value_search(img, x1, y1, rnd_black, bbx[0])
            x1 = pixel_search(img, x1, y1, bbx[1], max_val)
    
            x2 = bbx[0] + x1
            y2 = bbx[1] + offset[1]
            w = bbx[0]/im_w_f
            h = bbx[1]/im_h_f
            cx = (x1 + 0.5 * bbx[0])/im_w_f
            cy = (y1 + 0.5 * bbx[1])/im_h_f

            # draw.rectangle([x1, y1, x2, y2], outline='red')
            bbx = (x1, y1, x2, y2)
            bbxs.append(bbx)

            offset[0] = x2

        for idx, bbx in enumerate(bbxs):
            x1, y1, x2, y2 = bbx
            draw.rectangle([x1, y1, x2, y2], outline='red')

            # if idx > 21:
                # print "x1: {}, y1: {}, x2: {}, y2: {}".format(x1, y1, x2, y2)
                # img.show()
                # dl_pic = raw_input("Delete {}? [y/N]: ".format(font_path))

        # font_name = os.path.basename(font_path).split(".")[0]
        # title = "{}_{}".format(font_name, count)
        # print title
        img.show()
        # dl_pic = raw_input("Delete {}? [y/N]: ".format(font_path))
