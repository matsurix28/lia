import cv2
import numpy as np


def rotate_horizontal(img, cnts):
    """Rotate image to be horizontal.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    cnts : [[int, int], ...]
        Contours of object.

    Returns
    -------
    rotated_img : numpy.ndarray
        Rotated image.
    """
    center, _, angle = cv2.fitEllipse(cnts)
    rotate_angle = angle - 90
    rotated_img = rotate(img, rotate_angle, center)
    return rotated_img


def rotate(img, angle, center):
    """Rotate image.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    angle : float
        Angle of rotation.
    center : (int, int)
        Coordinate of center.

    Returns
    -------
    rotated_img : numpy.ndarray
        Rotated image.
    """
    height, width = img.shape[:2]
    corners = np.array([(0, 0), (width, 0), (width, height), (0, height)])
    radius = np.sqrt(max(np.sum((center - corners) ** 2, axis=1)))
    frame = int(radius * 2)
    trans = cv2.getRotationMatrix2D(center, angle, 1)
    trans[0][2] += radius - center[0]
    trans[1][2] += radius - center[1]
    rotated_img = cv2.warpAffine(img, trans, (frame, frame))
    return rotated_img
