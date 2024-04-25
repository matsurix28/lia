"""Select the one with the clearest leaf outline in H, S, and V."""

import cv2
import numpy as np
from .get_cnts import get_cnts
from .evaluate_noise import evaluate_noise

def sort_hsv_cnts(img, thresh=60, blank_ratio=98, noise_ratio_thresh=50) -> list:
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
        cnts_list = get_cnts(img_bin)
        if len(cnts_list) == 0:
            continue
        num_noise, noise_ratio = evaluate_noise(image)
        if noise_ratio > noise_ratio_thresh:
            continue
        noise_list.append([num_noise, cnts_list])
    if len(noise_list) > 0:
        noise_list.sort(key=lambda x: x[0])
        sorted_cnts_list = [r[1] for r in noise_list]
        return sorted_cnts_list
    else:
        raise ValueError('No contours were detected.')
