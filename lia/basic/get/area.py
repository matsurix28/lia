import cv2
import numpy as np


def get_overlap_area(img1, img2):
    """Get overlap area.

    Parameters
    ----------
    img1 : numpy.ndarray
        Input image 1.
    img2 : numpy.ndarray
        Input image 2.

    Returns
    -------
    overlap_area
        Area of overlapping of two images.
    """
    and_img = cv2.bitwise_and(img1, img2)
    overlap_area = np.sum(and_img)
    return overlap_area


def get_mottle_area():
    pass
