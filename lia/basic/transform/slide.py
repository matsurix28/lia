import cv2

from lia.basic.transform.crop import crop_center


def slide_horizontal(img, distance):
    """Slide image horizontaly.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    distance : int
        Slide distance. If distance is plus value, slide right.

    Returns
    -------
    fill_img : numpy.ndarray
        Sliding image with gaps filled. This is the same size as input.

    Raises
    ------
    ValueError
        if distance is larger than image width.
    """
    height, width = img.shape[:2]
    if abs(distance) > width:
        raise ValueError("Too large distance.")
    size = (width - abs(distance), height)
    pos_x = distance / 2
    cropped_img = crop_center(img, size, pos_x=pos_x)
    fill_width = abs(distance)
    if distance > 0:
        fill_img = cv2.copyMakeBorder(
            cropped_img, 0, 0, fill_width, 0, cv2.BORDER_CONSTANT
        )
    elif distance < 0:
        fill_img = cv2.copyMakeBorder(
            cropped_img, 0, 0, 0, fill_width, cv2.BORDER_CONSTANT
        )
    else:
        fill_img = cropped_img
    return fill_img
