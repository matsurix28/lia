"""Extract leaf from an image."""

from lia.basic.evaluate import background
from lia.basic.evaluate._consts import CANNY_THRESH1, CANNY_THRESH2, NOISE_THRESH
from lia.basic.get._consts import (
    BEYOND_ERROR_ELLIPSE,
    BLANK_RATIO,
    DIFF_ELLIPSE_SIZE,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
    MIN_CNTS_RATIO,
    NOISE_RATIO_THRESH,
    THRESH,
    WHITE_BG_THRESH,
)
from lia.basic.get.cnts import get_cnts, get_cnts_from_hsv, get_cnts_white_background
from lia.basic.get.difference import get_diff_ellipse
from lia.basic.get.image import get_in_color_range
from lia.basic.get.object import get_center_object


def extract_leaf_by_thresh(
    img,
    thresh=THRESH,
    blank_ratio=BLANK_RATIO,
    noise_ratio_thresh=NOISE_RATIO_THRESH,
    min_cnts_ratio=MIN_CNTS_RATIO,
    canny_thresh1=CANNY_THRESH1,
    canny_thresh2=CANNY_THRESH2,
    noise_thresh=NOISE_THRESH,
    diff_ellipse_size=DIFF_ELLIPSE_SIZE,
    beyond_error_ellipse=BEYOND_ERROR_ELLIPSE,
    white_bg_thresh=WHITE_BG_THRESH,
):
    """Extract contours of leaf from an image by using threshold.

    Parameters
    ----------
    img : numpy.ndarray
        Input image.
    thresh : int, optional
        Threshold to detect contours.
    blank_ratio : int, optional
        Max ratio of blank area.
    noise_ratio_thresh : int, optional
        Threshold of noise contours.
    min_cnts_ratio : int, optional
        Ratio of minimum contours size.
    canny_thresh1 : int, optional
        Threshold 1 for canny.
    canny_thresh2 : int, optional
        Threshold 2 for canny.
    noise_thresh : int, optional
        Threshold for contours of noise.
    white_bg_threshold : int
        Threshold of binarization for white background.

    Returns
    -------
    leaf_candidates: list
        Contours list of leaf candidate.

    Raises
    ------
    ValueError
        If there are no centered contours.
    ValueError
        If leaf shape contours could not be detected.
    """
    # Check background color.
    if background.is_background_black(img):
        # Sort H, S, and V in order of clarity of leaf outline, and find contours from each
        cnts_list = get_cnts_from_hsv(
            img,
            thresh=thresh,
            blank_ratio=blank_ratio,
            noise_ratio_thresh=noise_ratio_thresh,
            min_cnts_ratio=min_cnts_ratio,
            canny_thresh1=canny_thresh1,
            canny_thresh2=canny_thresh2,
            noise_thresh=noise_thresh,
        )
    else:
        cnts_list = [get_cnts_white_background(img, white_bg_thresh, min_cnts_ratio)]
    # Get most centered contour.
    center_cnt_list = []
    for cnts in cnts_list:
        try:
            center_cnt = get_center_object(img, cnts)
        except:
            continue
        else:
            center_cnt_list.append(center_cnt)
    # Whether contour is leaf or not.
    if len(center_cnt_list) == 0:
        raise ValueError("There are no centered contours.")
    leaf_candidates = []
    for cnt in center_cnt_list:
        try:
            diff_ellipse = get_diff_ellipse(
                img, cnt, diff_ellipse_size, beyond_error_ellipse
            )
        except:
            continue
        else:
            leaf_candidates.append(cnt)
    if len(leaf_candidates) == 0:
        raise ValueError("Leaf shape contours could not be detected.")
    return leaf_candidates


def extract_leaf_by_color(
    img,
    lower=LEAF_COLOR_LOWER,
    upper=LEAF_COLOR_UPPER,
    color_format=LEAF_COLOR_FORMAT,
    min_cnts_ratio=MIN_CNTS_RATIO,
):
    """Extract leaf from image by color range.

    Parameters
    ----------
    img : numpy.ndarray
        Input color image.
    lower : (int, int, int)
        Lower of color.
    max : (int, int, int)
        Upper of color.
    color_format : str, optional
        Color format, HSV or RGB.

    Returns
    -------
    center : list
        Most centered leaf contours.

    Raises
    ------
    ValueError
        If invalid color format.
    """
    mask = get_in_color_range(img, lower=lower, upper=upper, color_format=color_format)
    cnts = get_cnts(mask, min_cnts_ratio=min_cnts_ratio)
    center = get_center_object(img, cnts)
    return center
