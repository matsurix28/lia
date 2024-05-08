import cv2
import numpy as np

from lia.basic.transform.crop import crop
from lia.basic.transform.slide import slide_horizontal


def align_shape_horizontal(std_img, var_img, width_range):
    if (not len(std_img.shape) == 2) or (not len(var_img.shape) == 2):
        raise ValueError("Input images should be binary image.")
    std_height, std_width = std_img.shape[:2]
    var_height, var_width = var_img.shape[:2]
    size = (std_width, std_height)
    if not std_height == var_height:
        var_img = cv2.resize(var_img, dsize=(var_width, std_height))
    overlay_list = []
    for fx_scale in range(-width_range, width_range, 1):
        fx = (100 + fx_scale) / 100
        resized_img = cv2.resize(var_img, dsize=None, fx=fx, fy=1)
        resized_width = resized_img.shape[1]
        diff_width = resized_width - std_width
        # koko kara you kento
        # ==========================================
        if diff_width > 0:
            side = diff_width / 2
            for pos_x in range(-side, side, 1):
                cropped_img = crop(resized_img, size, pos_x=pos_x)
                if std_img.shape == cropped_img.shape:
                    xor_img = cv2.bitwise_xor(std_img, cropped_img)
                    white = np.sum(xor_img)
                    overlay_list.append([white, fx, pos_x, None])
                else:
                    continue
        else:
            for pos_x in range(0, diff_width, 1):
                filled_img = cv2.copyMakeBorder()
                slided_img = slide_horizontal(resized_img)
        # =================================================
