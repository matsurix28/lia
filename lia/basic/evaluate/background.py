import cv2

from ._consts import BACKGROUND_AREA, BACKGROUND_THRESH


def is_background_black(img):
    """Check if the background color is black or white.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.

    Returns
    -------
    True
        Background is black.
    False
        Background is white.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(img_gray, BACKGROUND_THRESH, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    std_area = img.shape[0] * img.shape[1] * BACKGROUND_AREA
    big = list(filter(lambda x: cv2.contourArea(x) > std_area, cnts))
    if len(big) > 0:
        return False
    else:
        return True
