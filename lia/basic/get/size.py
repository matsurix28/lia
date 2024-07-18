def get_max_size(img):
    """Get max height and width of object.

    Parameters
    ----------
    img : numpy.ndarray
        Input binary image.

    Returns
    -------
    max_height : int
        Max height of object.
    max_width : int
        Max width of object.
    """
    thresh = img.max()
    heights = (img == thresh).sum(axis=0)
    widths = (img == thresh).sum(axis=1)
    max_height = heights.max()
    max_width = widths.max()
    return max_height, max_width
