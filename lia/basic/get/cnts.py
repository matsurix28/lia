import cv2

from . import MIN_CNTS_RATIO


def get_cnts(img, min_cnts_ratio=MIN_CNTS_RATIO):
    """Get contours list from binary image.

    Parameters
    ----------
    img : numpy.ndarray
        Input binary image.
    min_ratio : int (default: 100)
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
