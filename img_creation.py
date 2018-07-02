#!/usr/bin/python
import os
import sys
import fnmatch
import argparse
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

def pixel_search_x(img, x_coord, y_coord, height, img_height, max_val, direction):
    y_initial = y_coord
    y_final = y_coord + height

    while y_coord < y_final and y_coord < img_height:
        if img.getpixel((x_coord, y_coord)) < max_val:  # does not match background values
            if direction == 'left':
                x_coord -= 0.1  # shift to the left
            else:
                x_coord += 0.1  # shift to the right
            y_coord = y_initial

        y_coord += 0.1

    return x_coord

def pixel_search_y(img, x_coord, y_coord, width, height, img_width, img_height, max_val):
    y_next = y_coord
    y_coord = y_coord - 0.1
    y_initial = y_coord
    x_initial = x_coord
    y_final = y_coord + height
    x_final = x_coord + width

    while y_next < y_final and y_next < img_height:
        while x_coord < x_final and x_coord < img_width:
            if img.getpixel((x_coord, y_next)) < max_val:  # does not match background values
                return y_coord
            x_coord = x_coord + 0.01

        y_coord += 0.1
        y_next = y_coord + 0.1
        x_coord = x_initial

    return y_coord

# TODO: don't do extra checks if intersection found along one line
def check_bbx_for_intersection(x1, y1, x2, y2, img, font_colour, label):
    intersection_found = False

    x_current = x1
    while x_current < x2: # check bottom horizontal line
        if img.getpixel((x_current, y1)) == font_colour:  # does not match background values
            intersection_found = True
            print "intersection along x line and y1: {}".format(img.getpixel((x_current, y1)))
            break
        x_current = x_current + 0.1

    x_current = x1
    while x_current < x2: # check top horizontal line
        if img.getpixel((x_current, y2)) == font_colour:  # does not match background values
            intersection_found = True
            print "intersection along x line and y2: {}".format(img.getpixel((x_current, y2)))
            break
        x_current = x_current + 0.1

    y_current = y1
    while y_current < y2: # check left vertical line
        if img.getpixel((x1, y_current)) == font_colour:  # does not match background values
            intersection_found = True
            print "intersection along left vertical line: {}".format(img.getpixel((x1, y_current)))
            break
        y_current = y_current + 0.1

    y_current = y1
    while y_current < y2: # check right vertical line
        if img.getpixel((x2, y_current)) == font_colour:  # does not match background values
            intersection_found = True
            print "intersection along right vertical line: {}".format(img.getpixel((x1, y_current)))
            break
        y_current = y_current + 0.1

    if intersection_found:
        img.show()
        print "Intersection found - " + label

def get_argparser():
    aparser = argparse.ArgumentParser(description="create OCR data...")
    aparser.add_argument('-cb', '--check-bbxs', action='store_true', help="check bounding box perimeter for an intersection with character, display image if intersection exists.")
    aparser.add_argument('-p', '--produce', help="produce output images for training to this path")
    aparser.add_argument('-o', '--outline', action='store_true', help="outline characters with red box")

    return aparser


if __name__ == "__main__":
    parser = get_argparser();
    args = parser.parse_args();

    if (os.path.isfile('font_data.csv')):
        font_data = pd.read_csv('font_data.csv', sep=',')
        fonts = font_data[(font_data.rating != 0)].font.tolist()

    for fcount, font_path in enumerate(fonts):
        # Need all chars in each font, upper and lower.
        for idx in range(0, 52):
            if idx < 25:
                char = chars_lower[idx]
            else:
                char = chars_upper[idx - 26]
            
            font_size = randint(30, 150)

            # Randomize shade of black
            rnd_shade = randint(0, 20)
            rnd_red = rnd_shade + randint(0, 2)
            rnd_blue = rnd_shade + randint(0, 2)
            rnd_green = rnd_shade + randint(0, 2)
            rnd_alpha = randint(240, 255)

            rnd_black = (rnd_red, rnd_blue, rnd_green, rnd_alpha)

            # TODO: run on all fonts

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

            draw.text((txtx, txty), char, fill=rnd_black, font=font)

            x1 = txtx
            y1 = txty
            y2 = y1 + bbx[1]

            max_val = max_value_search(img, x1, y1, rnd_black, bbx[0])
            x1 = pixel_search_x(img, x1, y1, bbx[1], im_h, max_val, 'left')
            y1 = pixel_search_y(img, x1, y1, bbx[0], bbx[1], im_w, im_h, max_val)
            x2 = pixel_search_x(img, x1 + bbx[0], y1, bbx[1], im_h, max_val, 'right')

            w = bbx[0]/im_w_f
            h = bbx[1]/im_h_f
            cx = (x1 + 0.5 * bbx[0])/im_w_f
            cy = (y1 + 0.5 * bbx[1])/im_h_f

            if (args.outline):
                draw.rectangle([x1, y1, x2, y2], outline='red')

            label = "font: {} char: {} - {} {} {} {} -- colour: {}".format(font_path, idx, cx, cy, w, h, rnd_black)

            if (args.check_bbxs):
                check_bbx_for_intersection(x1, y1, x2, y2, img, rnd_black, label)
            elif (args.produce):
                # Blur image
                rnd_blur = rnd_uniform(0.0, 5.0) * im_h_f/1000
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
                font_name = os.path.basename(font_path).split('.')[0]
                img_name = "{}_{}.png".format(font_name, idx);
                img_path = os.path.join(args.produce, img_name)

                img.save(img_path, "PNG", dpi=(600, 600))
                # img.show()
            else:
                sys.exit("please provide an argument (-cb, or -p)");

            if idx == 51:
                print "completed ({}/{}): {}".format(fcount, len(fonts), font_path)

