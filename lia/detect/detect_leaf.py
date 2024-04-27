"""Extract leaf from an image."""

import re

import cv2

from lia.basic.get import get_center_object, get_cnts, get_hsv_cnts


def extract_leaf_by_thresh(img, thresh=30):
    """Get contours of leaf candidate.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    thresh : int, (default: 30)
        Threshold to get contours.

    Returns
    -------
    leaf_candidates: list
        Contours list of leaf candidate.

    Raises
    ------
    ValueError
        If there are no centered contours.
    ValueError
        If leaf shape contours could not be detected.
    """

    # Sort H, S, and V in order of clarity of leaf outline, and find contours from each
    cnts_list = get_hsv_cnts(img, thresh)
    # Get most centered contour.
    center_cnt_list = []
    for cnts in cnts_list:
        try:
            center_cnt = get_center_object(img, cnts)
        except:
            continue
        else:
            center_cnt_list.append(center_cnt)
    # Whether contour is leaf or not.
    if len(center_cnt_list) == 0:
        raise ValueError("There are no centered contours.")
    leaf_candidates = []
    for cnt in center_cnt_list:
        try:
            diff_ellipse = diff_ellipse(img, cnt)
        except:
            continue
        else:
            leaf_candidates.append(cnt)
    if len(leaf_candidates) == 0:
        raise ValueError("Leaf shape contours could not be detected.")
    return leaf_candidates


def extract_leaf_by_color(img, min, max, color_format="HSV"):
    """Extract leaf from image by color range.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    min : tuple
        Lower of color.
    max : tuple
        Upper of color. (ex. (50, 100, 200))
    color_format : str, (default: "HSV")
        Color format, HSV or RGB.

    Returns
    -------
    center : list
        Most centered leaf contours.

    Raises
    ------
    ValueError
        If invalid color format.
    """
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
    center = get_center_object(img, cnts)
    return center
