import cv2
import numpy as np

from lia.basic.transform.crop import crop_left
from lia.basic.transform.slide import slide_horizontal


def get_align_hori_func(std_img, var_img, width_range, slide_ratio):
    """Scale and move horizontally to align images.

    Parameters
    ----------
    std_img : numpy.ndarray
        Standard image.
    var_img : numpy.ndarray
        Input image to be scaled.
    width_range : int
        Scaling factor.
    slide_ratio : int
        Percentage to move.

    Returns
    -------
    transhape: function
        Scale and move function.

    Raises
    ------
    ValueError
        If input image is not binary image.
    ValueError
        If height of images are different.
    ValueError
        If contours don't overlap.
    """
    if (not len(std_img.shape) == 2) or (not len(var_img.shape) == 2):
        raise ValueError("Input images should be binary image.")
    std_height, std_width = std_img.shape[:2]
    var_height, var_width = var_img.shape[:2]
    size = (std_width, std_height)
    if not std_height == var_height:
        raise ValueError("Height of image is different.")
    overlay_list = []
    for fx_scale in range(-width_range, width_range, 1):
        fx = (100 + fx_scale) / 100
        resized_img = cv2.resize(var_img, dsize=None, fx=fx, fy=1)
        resized_width = resized_img.shape[1]
        diff_width = resized_width - std_width
        if diff_width > 0:
            base_img = cv2.copyMakeBorder(
                std_img, 0, 0, 0, diff_width, cv2.BORDER_CONSTANT
            )
            over_img = resized_img.copy()
        else:
            base_img = std_img.copy()
            over_img = cv2.copyMakeBorder(
                resized_img, 0, 0, 0, abs(diff_width), cv2.BORDER_CONSTANT
            )
        slide_range = int(slide_ratio / 100 * resized_width)
        for slide_distance in range(-slide_range, slide_range, 1):
            slided_img = slide_horizontal(over_img, slide_distance)
            xor_img = cv2.bitwise_xor(base_img, slided_img)
            white = np.sum(xor_img)
            result = {
                "not_overlay": white,
                "size": resized_img.shape[:2],
                "slide": slide_distance,
                "diff_width": diff_width,
            }
            overlay_list.append(result)
    if len(overlay_list) > 0:
        best = min(overlay_list, key=lambda x: x["not_overlay"])
    else:
        raise ValueError("Cannot overlay.")
    re_height, re_width = resized_img.shape[:2]
    if best["diff_width"] > 0:

        def transhape(input_img):
            trans_height, trans_width = best["size"]
            re_img = cv2.resize(input_img, dsize=(trans_width, trans_height))
            slide = best["slide"]
            re_slided_img = slide_horizontal(re_img, slide)
            re_cropped_img = crop_left(re_slided_img, std_width)
            return re_cropped_img

        return transhape
    else:

        def transhape(input_img):
            trans_height, trans_width = best["size"]
            re_img = cv2.resize(input_img, dsize=(trans_width, trans_height))
            re_fill_img = cv2.copyMakeBorder(
                re_img, 0, 0, 0, abs(best["diff_width"]), cv2.BORDER_CONSTANT
            )
            slide = best["slide"]
            re_slided_img = slide_horizontal(re_fill_img, slide)
            return re_slided_img

        return transhape
