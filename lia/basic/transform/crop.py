def crop_center(img, size, pos_x=0, pos_y=0):
    """Crop imgae.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    size : (int, int)
        Crop size, (width, height).
    pos_x : int, optional
        Center of x axis.
    pos_y : int, optional
        Center of y axis.

    Returns
    -------
    cropped_img : numpy.ndarray
        Cropped image.
    """
    height, width = img.shape[:2]
    size_x = int(size[0])
    size_y = int(size[1])
    cropped_img = img[
        int(height / 2 - size_y / 2 - pos_y) : int(height / 2 + size_y / 2 - pos_y),
        int(width / 2 - size_x / 2 - pos_x) : int(width / 2 + size_x / 2 - pos_x),
    ]
    return cropped_img


def crop_left(img, width):
    """Crop left.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    width : int
        Crop width.

    Returns
    -------
    cropped_img : numpy.ndarray
        Cropped image.
    """
    height = img.shape[0]
    cropped_img = img[0:height, 0:width]
    return cropped_img
