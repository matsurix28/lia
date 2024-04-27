import re

import cv2

from . import LEAF_COLOR_FORMAT, LEAF_COLOR_LOWER, LEAF_COLOR_UPPER


def get_in_color_range(
    img, lower=LEAF_COLOR_LOWER, upper=LEAF_COLOR_UPPER, color_format=LEAF_COLOR_FORMAT
):
    if color_format.lower() == "hsv":
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, lower, upper)
    elif re.match("bgr|rgb", color_format.lower()):
        mask = cv2.inRange(img, lower, upper)
    else:
        raise ValueError(
            f'Invalid color format: {color_format}\nPlease select "RGB" or "HSV".'
        )
    return mask
