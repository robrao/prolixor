#!/usr/bin/python
import io
import os
import csv
import psutil
import fnmatch

from random import randint, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from collections import deque
from string import ascii_lowercase as chars_lower
from string import ascii_uppercase as chars_upper
from skimage.util import random_noise
from random import uniform as rnd_uniform

import numpy as np


def cast_to_int(var):
    try:
        if var == '0':
            res = 1
        else:
            res = int(var)
    except Exception as e:
        res = 0
    return res

def csv_exists():
    return os.path.isfile('./font_ratings.csv')

def write_ratings_to_file(font_paths):
    with open("font_ratings.csv", "wb") as outcsv:
        writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["font", "rating"])
        for fpr in font_paths:
            writer.writerow([fpr[0], fpr[1]])

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

    fonts_ratings = []
    if csv_exists():
        with open('font_ratings.csv', 'r') as csvfile:
            creader = csv.reader(csvfile, delimiter=',')
            for row in creader:
                if row[0] == 'font' and row[1] == 'rating':
                    continue
                fonts_ratings.append((row[0], row[1]))

    for idx, font_path in enumerate(fonts):
        if idx < len(fonts_ratings) and fonts_ratings[idx][0] == font_path:
            print "{} -- {}".format(font_path, fonts_ratings[idx][1])
            continue

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
        im_w_f = font_size * 2
        im_h_f = font_size + im_w_f
        im_w = int(im_w_f)
        im_h = int(im_h_f)

        # randomize background on image
        try:
            img = Image.new('RGBA', (im_w, im_h), 'white')
            draw = ImageDraw.Draw(img, "RGBA")
            dw, dh = draw.textsize(c_lower, font=font)
            img2 = Image.new('RGBA', (im_w, im_h), 'white')
            draw2 = ImageDraw.Draw(img2, "RGBA")
            dw, dh = draw2.textsize(c_upper, font=font)
        except IOError as e:
            print "{} corrupt".format(font_path)
            fonts_ratings.append((font_path, 0))
            continue

        try:
            cent_w = (im_w - dw) / 2.0
            cent_h = (im_h - dh) / 2.0
            x_jitter = randint(0, int((im_w - dw) * 0.25)) * choice([-1, 1])
            y_jitter = randint(0, int((im_h - dh) * 0.25)) * choice([-1, 1])
            txtx = cent_w + x_jitter
            txty = cent_h + y_jitter
        except ValueError as e:
            print "Error: test dw > img width -- ignoring..."
            continue

        draw.text((txtx, txty), c_lower, fill="black", font=font)
        draw2.text((txtx, txty), c_upper, fill="black", font=font)

        #TODO: display images so they are not overlapped
        img.show(title="lower_case")
        img2.show(title="upper_case")

        format_string = "({}/{}) Rate font [0 - 5]: ".format(idx, len(fonts))
        rating = raw_input(format_string);
        is_int = cast_to_int(rating)

        while not is_int:
            if rating == 'w':
                write_ratings_to_file(fonts_ratings)
                print "saved to file"
            rating = raw_input(format_string)
            is_int = cast_to_int(rating)


        fonts_ratings.append((font_path, rating))

        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

    write_ratings_to_file(fonts_ratings)
