import cv2

from lia.basic.get.consts import WHITE_INV_THRESH


def get_white_bg_binary_img(img, thresh=WHITE_INV_THRESH):
    """Get binary iamge from white background image.

    Parameters
    ----------
    img : numpy.ndarray
        Input white background image.
    thresh : int
        Threshold of white background.

    Returns
    -------
    binary_img : numpy.ndarray
        Binary image.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY_INV)
    return binary_img
