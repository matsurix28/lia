import cv2
import numpy as np

from . import (
    BLANK_RATIO,
    CANNY_THRESH1,
    CANNY_THRESH2,
    MIN_CNTS_RATIO,
    NOISE_RATIO_THRESH,
    NOISE_THRESH,
    THRESH,
)
from .cnts import get_cnts
from .noise import get_noise


def get_hsv_cnts(
    img,
    thresh=THRESH,
    blank_ratio=BLANK_RATIO,
    noise_ratio_thresh=NOISE_RATIO_THRESH,
    min_cnts_ratio=MIN_CNTS_RATIO,
    canny_thresh1=CANNY_THRESH1,
    canny_thresh2=CANNY_THRESH2,
    noise_thresh=NOISE_THRESH,
):
    """Sort H, S, and V in order of clarity of leaf outline.

    Parameters
    ----------
    img : numpy.ndarray
        Input BGR image
    thresh : int
        Minimum threshold
    noise_ratio : int (default: 98)
        Max percentage of screen occupied by noise.

    Returns
    -------
    sorted_cnts_list : list
        lList of contours of H, S, and V in order of decreasing noise.

    Raises
    ------
    ValueError
        If no contours were detected.
    """
    height, width = img.shape[:2]
    area = height * width
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.split(img_hsv)
    noise_list = []
    for image in hsv:
        _, img_bin = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
        white = int(np.sum(img_bin) / 255)
        black = area - white
        if ((white / area) * 100 > blank_ratio) or ((black / area) * 100 > blank_ratio):
            continue
        cnts_list = get_cnts(img_bin, min_cnts_ratio)
        if len(cnts_list) == 0:
            continue
        num_noise, noise_ratio = get_noise(
            image, canny_thresh1, canny_thresh2, noise_thresh
        )
        if noise_ratio > noise_ratio_thresh:
            continue
        noise_list.append([num_noise, cnts_list])
    if len(noise_list) > 0:
        noise_list.sort(key=lambda x: x[0])
        sorted_cnts_list = [r[1] for r in noise_list]
        return sorted_cnts_list
    else:
        raise ValueError("No contours were detected.")
