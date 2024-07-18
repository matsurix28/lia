import colorsys


def rgb2hsv(red, green, blue):
    """Convert RGB to HSV.

    Parameters
    ----------
    red : int
        Red.
    green : int
        Green.
    blue : int
        Blue.

    Returns
    -------
    hue : float
        Hue.
    saturation : float
        Saturation.
    value : int
        Value.
    """
    hsv = colorsys.rgb_to_hsv(red, green, blue)
    hue = hsv[0] * 360
    saturation = hsv[1] * 255
    value = hsv[2]
    return hue, saturation, value
