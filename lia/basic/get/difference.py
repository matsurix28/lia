import cv2
import numpy as np

from ._consts import BEYOND_ERROR_ELLIPSE, DIFF_ELLIPSE_SIZE


def get_diff_ellipse(
    img,
    cnt,
    diff_ellipse_size=DIFF_ELLIPSE_SIZE,
    beyond_error_rate=BEYOND_ERROR_ELLIPSE,
):
    """Get difference from approximate ellipse.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    cnt : list
        List of contour point.
    diff_ellipse_size : int
        Tolerance for difference between approximate ellipse and contour.
    beyond_error_ellipse : int
        Percentage of approximate ellipses that extend beyond the image.

    Returns
    -------
    xor_area : int
        Difference between the area of the contours and the area of the approximate ellipse.

    Raises
    ------
    Exception
        Cannot fit ellipse.
    ValueError
        THe approximation is incorrect, too far.
    ValueError
        Approximate ellipse extend beyond the image.
    """

    ellipse = cv2.fitEllipse(cnt)
    height, width = img.shape[:2]
    x, y = ellipse[0]
    ellipse_height, ellipse_width = ellipse[1]
    img_ellipse = np.zeros(img.shape[:3], np.uint8)
    img_cnts = np.zeros(img.shape[:3], np.uint8)
    cv2.ellipse(img_ellipse, ellipse, (255, 255, 255), -1)
    cv2.drawContours(img_cnts, [cnt], -1, (255, 255, 255), -1)
    # Difference between the area of the contours and the area of the approximate ellipse.
    img_and = cv2.bitwise_and(img_ellipse, img_cnts)
    img_xor = cv2.bitwise_xor(img_and, img_ellipse)
    diff_area = int(np.sum(img_xor) / 255 / 3)
    ellipse_area = np.sum(img_ellipse) / 255 / 3
    # Whether the ellipse extends beyond the image or not.
    size_error = 1 + (beyond_error_rate / 100)
    if (
        (np.abs(height / 2 - y) + (ellipse_height / 2)) < (height / 2 * size_error)
    ) and ((np.abs(width / 2 - x) + (ellipse_width / 2)) < (width / 2 * size_error)):
        diff_ratio = abs(int(diff_area / ellipse_area * 100))
        if diff_ratio < diff_ellipse_size:
            return diff_ratio
        else:
            raise ValueError("The approximation is incorrect.")
    else:
        raise ValueError("Approximate ellipses extend well beyond the image.")
