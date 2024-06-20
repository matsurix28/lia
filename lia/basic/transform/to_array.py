def to_color_array(img):
    """Reshape from image to array of color.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    color_array : [[int], ...] or [[int, int, int], ...]
        Array of colors. BGR, grayscale, or binary.
    """
    height, width = img.shape[:2]
    length = height * width
    if img.ndim == 3:
        num_color = img.shape[2]
        color_array = img.reshape(length, num_color)
    elif img.ndim == 2:
        color_array = img.reshape(length)
    return color_array
