import cv2
import numpy as np


def get_center_object(img, cnts):
    """Obtain the most centered contour in the image.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    cnts : list
        List of contours.

    Returns
    -------
    main_object
        Most centered contour.

    Raises
    ------
    ValueError
        If there are no contours in input.
    ValueError
        If cannot obtain centered contour.
    """
    if len(cnts) == 0:
        raise ValueError("There is no contours.")
    height, width = img.shape[:2]
    center = np.array([int(width / 2), int(height / 2)])
    min_dist = None
    main_obj = None
    is_first = True
    for cnt in cnts:
        moment = cv2.moments((cnt))
        try:
            cx = int(moment["m10"] / moment["m00"])
            cy = int(moment["m01"] / moment["m00"])
        except:
            continue
        center_cnt = np.array([cx, cy])
        dist = np.linalg.norm(center - center_cnt)
        if is_first:
            min_dist = dist
            main_obj = cnt
            is_first = False
        elif dist < min_dist:
            min_dist = dist
            main_obj = cnt
    if main_obj is not None:
        return main_obj
    else:
        raise ValueError("Could not find the central object.")
