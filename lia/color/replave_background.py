import cv2

THRESH = 230


def blackening_bg(img):
    """Change background color white to black.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.

    Returns
    -------
    black_img : numpy.ndarray
        Black background image.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(img_gray, THRESH, 255, cv2.THRESH_BINARY_INV)
    # black_img = cv2.bitwise_and(img, img, mask=bin)
    black_img = cv2.bitwise_not(img)
    return black_img
