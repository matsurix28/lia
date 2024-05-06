import cv2

# from . import MIN_CNTS_RATIO
from .consts import MIN_CNTS_RATIO, WHITE_BG_THRESH


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


def get_cnts_white_background(img, min_cnts_ratio=MIN_CNTS_RATIO):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_inv = cv2.bitwise_not(img_gray)
    _, bin = cv2.threshold(img_gray_inv, WHITE_BG_THRESH, 255, cv2.THRESH_BINARY)
    cnts_list = get_cnts(bin, min_cnts_ratio)
    return cnts_list
