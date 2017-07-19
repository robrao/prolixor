#!/usr/bin/python
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from collections import deque
from string import ascii_lowercase as chars_lower
from skimage.util import random_noise
from random import uniform as rnd_uniform

import numpy as np

'''
PERSPECTIVE NOTES:
    - stackoverflow: https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
    - ubc notes on trans: http://www.math.ubc.ca/~cass/graphics/Perspective.pdf
    - PIL image transform: http://pillow.readthedocs.io/en/3.4.x/reference/Image.html#PIL.Image.Image.transform

ISSUES:
    - This will require adjustments to bounding box points
        -- Should be able to apply the same transformation to bbx points
        and get updated bbx points
'''

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

for i in [0]:
    font = ImageFont.truetype("/Users/robbyrao/Downloads/Roboto/Roboto-Black.ttf", size=font_size)

# font size need to change in relation to image size
buff_size = font_size * num_chars * 0.5  # allow crop of image after transform

im_w_f = font_size * num_chars * 0.61 + buff_size
im_h_f = font_size + im_w_f * 0.1
im_w = int(im_w_f)
im_h = int(im_h_f)

# randomize background on image
img = Image.new('RGBA', (im_w, im_h), 'white')
draw = ImageDraw.Draw(img, "RGBA")
dw, dh = draw.textsize(word, font)

# per char size
char_size = []
for c in chars:
    w, h = draw.textsize(c, font)
    csize = (w, h)
    char_size.append(csize)

cent_w = (im_w - dw) / 2.0
cent_h = (im_h - dh) / 2.0
x_jitter = randint(0, int((im_w - dw) * 0.25)) * choice([-1, 1])
y_jitter = randint(0, int((im_h - dh) * 0.25)) * choice([-1, 1])
txtx = cent_w + x_jitter
txty = cent_h + y_jitter

draw.text((txtx, txty), word, rnd_black, font=font)

offset = [txtx, txty]
labels = []

# these will be needed be recalculated after translation
# should be able to use transformation formula to find
# corners [x1, y1, x2, y2]
for idx, bbx in enumerate(char_size):
    x1 = offset[0]
    y1 = offset[1]
    x2 = offset[0] + bbx[0]
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
          npim, 'speckle', mean=rnd_uniform(0, 2), var=rnd_uniform(0.01, 0.1)
)
res = npim * noise
img = Image.fromarray(np.uint8(res))

# Perspective manipulation
m = rnd_uniform(-1, 1)
print("m: {}".format(m))
width, height = img.size
xshift = abs(m) * width
new_width = width + int(round(xshift))
# can do transform with tf.contrib.image.transform (also can do batch)
# does it same manner

# tilt left or right, still need to tilt up and down
img = img.transform((new_width, height), Image.AFFINE,
                    data=(1, m, -xshift if m > 0 else 0, 0, 1, 0),
                    resample=Image.BICUBIC)

if m < 0:
    pass
    # use bottom left corner, and top right corner for cropping
elif m > 0:
    pass
    # use top left corner, and bottom right corner for cropping

'''
Possible method for rotation

import tensorflow as tf
from PIL import Image

image_decoded = tf.image.decode_jpeg(tf.read_file('imgname.jpg'), channels=3)
pim = Image.open('imgname.jpg')
rot_im = tf.contrib.image.angles_to_projective_transforms(45, pim.size[1], pim.size[0])
enc = tf.image.encode_jpeg(cropped)
fname = tf.constant('2.jpg')
fwrite = tf.write_file(fname, enc)

sess = tf.Session()
result = sess.run(fwrite)
'''

for lbl in labels:
    print lbl

img.save("imgname.jpg", "JPEG", dpi=(600, 600))
