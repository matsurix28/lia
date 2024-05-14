import cv2
import numpy as np

from lia.basic.transform.crop import crop_center
from lia.basic.transform.slide import slide_horizontal


def align_shape_horizontal(std_img, var_img, width_range, slide_range):
    if (not len(std_img.shape) == 2) or (not len(var_img.shape) == 2):
        raise ValueError("Input images should be binary image.")
    std_height, std_width = std_img.shape[:2]
    var_height, var_width = var_img.shape[:2]
    size = (std_width, std_height)
    if not std_height == var_height:
        scale = std_height / var_height
        var_img = cv2.resize(var_img, dsize=None, fx=scale, fy=scale)
    overlay_list = []
    for fx_scale in range(-width_range, width_range, 1):
        fx = (100 + fx_scale) / 100
        resized_img = cv2.resize(var_img, dsize=None, fx=fx, fy=1)
        resized_width = resized_img.shape[1]
        diff_width = resized_width - std_width
        # koko kara you kento
        # ==========================================
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
        for slide_ratio in range(-slide_range, slide_range, 1):
            slide_distance = int(slide_ratio / 100 * resized_width)
            slided_img = slide_horizontal(over_img, slide_distance)
            xor_img = cv2.bitwise_xor(base_img, slided_img)
            white = np.sum(xor_img)
            result = {
                "not_overlay": white,
                "fx": fx,
                "slide": slide_distance,
                "diff_width": diff_width,
            }
            overlay_list.append(result)
    if len(overlay_list) > 0:
        best = min(overlay_list, key=lambda x: x["not_overlay"])
    else:
        raise ValueError('Cannot overlay.')
    if best["diff_width"] > 0:
        def transhape(img):

        # =================================================
