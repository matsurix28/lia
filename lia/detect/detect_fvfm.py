import itertools
import re
import statistics

import cv2
import numpy as np

from lia.basic.get._consts import WHITE_INV_THRESH
from lia.basic.get.cnts import get_cnts
from lia.basic.get.image import get_white_bg_binary_img

BAR_AREA_RATIO = 100


def read_fvfm_value(img):
    """Read Fv/Fm value from image.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    fvfm_value_list : [[float, int], ...]
        List of position height and Fv/Fm value.

    Raises
    ------
    ValueError
        If less than 2 value.
    """
    import easyocr

    reader = easyocr.Reader(["en"])
    text = reader.readtext(img)
    fvfm_value_list = []
    for word in text:
        if re.compile("0(\.|,)\d{2}$").match(word[1]):
            pos = (word[0][3][1] - word[0][0][1]) / 2 + word[0][0][1]
            value = float(word[1].replace(",", "."))
            fvfm_value_list.append([pos, value])
    if len(fvfm_value_list) >= 2:
        fvfm_value_list.sort(key=lambda x: x[0])
        return fvfm_value_list
    else:
        raise ValueError("Cannot find Fv/Fm value.")


def calculate_scale(fvfm_value_list):
    """Calculate height per fvfm value 1 from value.

    Parameters
    ----------
    fvfm_value_list : [[float, int], ...]
        List of position hight and Fv/Fm value.

    Returns
    -------
    scale : float
        Standard scale of Fv/Fm value.

    Raises
    ------
    ValueError
        If no value.
    """
    scale_list = []
    for pair in itertools.combinations(fvfm_value_list, 2):
        pos_diff = np.abs(pair[1][0] - pair[0][0])
        val_diff = np.abs(pair[0][1] - pair[1][1])
        scale = pos_diff / val_diff
        scale_list.append(scale)
    if len(scale_list) > 0:
        scale = statistics.median(scale_list)
        return scale
    else:
        raise ValueError("Cannot calculate scale. Not enough value.")


def get_bar_area(img, white_inv_thresh=WHITE_INV_THRESH, bar_area_ratio=BAR_AREA_RATIO):
    """Get Fv/Fm scale bar.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    white_inv_thresh : int, optional
        Threshold of white background.
    bar_area_ratio : int, optional
        Ratio of minimum bar size.

    Returns
    -------
    bar_area : [int, int, int, int]
        Bar area rectangle.

    Raises
    ------
    ValueError
        Cannot find scale bar.
    """
    binary_img = get_white_bg_binary_img(img, white_inv_thresh)
    cnts = get_cnts(binary_img, bar_area_ratio)
    img_height = img.shape[0]
    for cnt in cnts:
        x, y, width, height = cv2.boundingRect(cnt)
        ratio = height / width
        occupancy = height / img_height
        if (ratio > 0.7) and (occupancy > 0.8):
            return [x, y, width, height]
    raise ValueError("Cannot find scalebar.")


def get_fvfm_list(
    img, white_inv_thresh=WHITE_INV_THRESH, bar_area_ratio=BAR_AREA_RATIO
):
    """Get list of color and Fv/Fm value.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    fvfm_color_list : [[int, int, int], ...]
        List of Fv/Fm scale color.
    fvfm_value_lsit : [int, ...]
        List of Fv/Fm scale value.

    Raises
    ------
    ValueError
        Cannot get Fv/Fm value.
    """
    bar_area = get_bar_area(img, white_inv_thresh, bar_area_ratio)
    top = bar_area[1]
    bottom = bar_area[1] + bar_area[3]
    center_x = int(bar_area[0] + (bar_area[2] / 2))
    fvfm_value_list = read_fvfm_value(img)
    std_fvfm_pos_y = fvfm_value_list[0][0]
    std_fvfm_val = int(fvfm_value_list[0][1] * 1000)
    scale_fvfm_list = [[x[0], int(x[1] * 1000)] for x in fvfm_value_list]
    scale = calculate_scale(scale_fvfm_list)
    upper_num = int((std_fvfm_pos_y - top) / scale)
    lower_num = int((bottom - std_fvfm_pos_y) / scale)
    fvfm_list = []
    for i in range(1, upper_num + 1):
        fvfm_value = std_fvfm_val + i
        pos_y = int(std_fvfm_pos_y - (i * scale))
        color = img[pos_y, center_x].tolist()
        fvfm_list.append([color, fvfm_value / 1000])
    for i in range(1, lower_num + 1):
        fvfm_value = std_fvfm_val - i
        pos_y = int(std_fvfm_pos_y + (i * scale))
        color = img[pos_y, center_x].tolist()
        fvfm_list.append([color, fvfm_value / 1000])
    if len(fvfm_list) > 0:
        fvfm_list.sort(key=lambda x: x[1], reverse=True)
        fvfm_color_list = [x[0] for x in fvfm_list]
        fvfm_value_list = [x[1] for x in fvfm_list]
        return fvfm_color_list, fvfm_value_list
    else:
        raise ValueError("Cannot get Fv/Fm value.")
