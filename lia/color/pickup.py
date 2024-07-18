COLOR_THRESH1 = 0
COLOR_THRESH2 = 0


def pickup_over_thresh(
    color1, color2, color_thresh1=COLOR_THRESH1, color_thresh2=COLOR_THRESH2
):
    """Pick up from an array of colors that are both above the threshold.

    Parameters
    ----------
    color1 : [[int, int, int], ...]
        Array of color 1.
    color2 : [[int, int, int], ...]
        Array of color 2.
    color_thresh1 : int, optional
        Threshold for color 1.
    color_thresh2 : int, optional
        Threshold for color 2.

    Returns
    -------
    result1 : [[int, int, int], ...]
        Picked color 1.
    result2 : [[int, int, int], ...]
        Picked color 2.

    Raises
    ------
    ValueError
        Size of array are different.
    """
    if color1.shape[0] != color2.shape[0]:
        raise ValueError("Image size are different.")
    result1 = []
    result2 = []
    length = color1.shape[0]
    for i in range(length):
        if (color1[i].sum() > color_thresh1) and (color2[i].sum() > color_thresh2):
            result1.append(color1[i])
            result2.append(color2[i])
    return result1, result2
