import cv2
import numpy as np

from lia.basic.evaluate._consts import CANNY_THRESH1, CANNY_THRESH2, NOISE_THRESH
from lia.basic.evaluate.noise import get_noise

from ._consts import (
    BLANK_RATIO,
    MIN_CNTS_RATIO,
    NOISE_RATIO_THRESH,
    THRESH,
    WHITE_BG_THRESH,
)


def get_cnts(img, min_cnts_ratio=MIN_CNTS_RATIO):
    """Get contours list from binary image.

    Parameters
    ----------
    img : numpy.ndarray
        Input binary image.
    min_ratio : int
        Minimum area ratio (min_area = area / min_ratio).

    Returns
    -------
    cnts_list : list
        List of contours.
    """
    height, width = img.shape[:2]
    min_area = (height * width) / min_cnts_ratio
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
    return cnts_list


def get_cnts_from_hsv(
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


def get_cnts_white_background(
    img, white_bg_thresh=WHITE_BG_THRESH, min_cnts_ratio=MIN_CNTS_RATIO
):
    """Get contours list from white background image.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    white_bg_thresh : int
        Threshold of binarization for white background.
    min_cnts_ratio : int
        Minimum area ratio (min_area = area / min_ratio).

    Returns
    -------
    cnts_list : [(array[[[int, int]], ...], ...), ...]
        List of contours.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_inv = cv2.bitwise_not(img_gray)
    _, bin = cv2.threshold(img_gray_inv, white_bg_thresh, 255, cv2.THRESH_BINARY)
    cnts_list = get_cnts(bin, min_cnts_ratio)
    return cnts_list
