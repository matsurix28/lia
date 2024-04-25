
import numpy as np
import cv2

SIZE_ERROR = 1.05

def get_diff_ellipse(img, cnt, diff_size=0.2):
    """Get difference from approximate ellipse.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    cnt : list
        List of contour point.
    diff_size : float (default: 0.2)

    Returns
    -------
    xor_area : float
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
    try:
        ellipse = cv2.fitEllipse(cnt)
    except:
        raise
    height, width = img.shape[:2]
    x, y = ellipse[0]
    ellipse_height, ellipse_width = ellipse[1]
    img_ellipse = np.zeros(img.shape[:3], np.uint8)
    img_cnts = np.zeros(img.shape[:3], np.uint8)
    cv2.ellipse(img_ellipse, ellipse, (255, 255, 255), -1)
    cv2.drawContours(img_cnts, [cnt], -1 (255, 255, 255), -1)
    # Difference between the area of the contours and the area of the approximate ellipse.
    img_and = cv2.bitwise_and(img_ellipse, img_cnts)
    img_xor = cv2.bitwise_xor(img_and, img_ellipse)
    xor_area = np.sum(img_xor) / 255 / 3
    ellipse_area = np.sum(img_ellipse) / 255 / 3
    # Whether the ellipse extends beyond the image or not.
    if ((np.abs(height / 2 - y) + (ellipse_height / 2)) < (height / 2 * SIZE_ERROR)) and \
       ((np.abs(width / 2 - x) + (ellipse_width / 2)) < (width / 2 * SIZE_ERROR)):
        if abs(xor_area / ellipse_area) < diff_size:
            return xor_area
        else:
            raise ValueError('The approximation is incorrect.')
    else:
        raise ValueError('Approximate ellipses extend well beyond the image.')
