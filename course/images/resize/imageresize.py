"""imagesresize:  toolcat applicatie die images resized.
"""


import re
import os
from PIL import Image, ImageOps
from cStringIO import StringIO

from anet.core import fs
from anet.imagetools import imtools


def resize(source, target, max="1000K", dpi=None):
    if isinstance(max, basestring):
        max = max.upper()
        max = re.sub("[^1234567890MKG]", "", max)
        if "K" in max:
            m = 1024
        elif "M" in max:
            m = 1024 * 1024
        elif "G" in max:
            m = 1024 * 1024 * 1024
        else:
            m = 1
        max = int(re.sub("[^1234567890]", "", max)) * m
    fs.copy(source, target)
    if fs.size(target) < max:
        return
    fail = 128
    success = 0
    im = None
    while fs.size(target) > max:
        quality = (fail + success) // 2
        if quality < 1:
            break
        if quality <= success:
            break
        if quality >= fail:
            break
        if not im:
            im = Image.open(source)
        print quality
        if dpi:
            im.save(target, quality=quality, dpi=(int(dpi), int(dpi)))
        else:
            im.save(target, quality=quality)
        if fs.size(target) <= max:
            success = quality
        else:
            fail = quality


def thumbnail(source, target, box, crop, rounding_type=None, radius=20, border_width=0, border_color=0, thumb_background="white", drop_shadow_width=0, canvas_border_width=0, embed=False):
    if not source:
        return
    img = Image.open(source)

    if img.mode not in ('L', 'RGB'):
        img = img.convert('RGB')

    # preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
        factor *= 2
    if factor > 1:
        img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)
    # calculate the cropping box and get the cropped part
    if crop:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / box[0]
        hRatio = 1.0 * y2 / box[1]
        if hRatio > wRatio:
            y1 = int(y2 / 2 - box[1] * wRatio / 2)
            y2 = int(y2 / 2 + box[1] * wRatio / 2)
        else:
            x1 = int(x2 / 2 - box[0] * hRatio / 2)
            x2 = int(x2 / 2 + box[0] * hRatio / 2)
        img = img.crop((x1, y1, x2, y2))
    # Round corners
    if rounding_type:
        img = imtools.round_image(img, rounding_type=rounding_type, radius=int(radius), back_color=thumb_background)
    # Border
    if int(border_width) > 0:
        img = imtools.border_image(img, border_width=int(border_width), border_color=int(border_color))
    # Shadow
    if int(drop_shadow_width) > 0:
        img = imtools.drop_shadow_image(img, border=int(drop_shadow_width), background_color=thumb_background)
    # Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)
    # Paste the image on top of the background
    if embed:
        background = Image.new('RGB', box, thumb_background)
        w, h = img.size
        W, H = background.size
        x = (W - w) / 2
        y = (H - h) / 2
        imtools.paste(background, img, (x, y))
        if int(canvas_border_width) > 0:
            background = ImageOps.expand(background, border=int(canvas_border_width), fill='black')
        img = background.copy()
    # save
    temp_handle = StringIO()
    img.save(temp_handle, 'jpeg')
    temp_handle.seek(0)
    img.save(target, 'jpeg')
