"""Extract by specifying a range of colors"""

import re

import cv2

from .get_cnts import get_cnts


def extract_color(img, min, max, color_format="HSV"):
    if color_format.lower() == "hsv":
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, min, max)
    elif re.match("bgr|rgb", color_format.lower()):
        mask = cv2.inRange(img, min, max)
    else:
        raise ValueError(
            f'Invalid color format: {color_format}\nPlease select "RGB" or "HSV".'
        )
    cnts = get_cnts(mask)
    return cnts
