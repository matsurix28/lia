import cv2
import numpy as np

from lia.align.shape import align_shape_horizontal
from lia.basic.get.size import get_max_size
from lia.basic.transform.crop import crop_center
from lia.basic.transform.rotate import rotate_horizontal

SIZE_ERROR = 1.2
WIDTH_RANGE = 20
SLIDE_RANGE = 10


def align_leaf(
    std_img,
    var_img,
    std_cnt,
    var_cnt,
    size_error=SIZE_ERROR,
    width_range=WIDTH_RANGE,
    slide_range=SLIDE_RANGE,
):
    std_bin_img = np.zeros(std_img.shape[:2], dtype=np.uint8)
    var_bin_img = np.zeros(var_img.shape[:2], dtype=np.uint8)
    cv2.drawContours(std_bin_img, [std_cnt], 0, 255, -1)
    cv2.drawContours(var_bin_img, [var_cnt], 0, 255, -1)
    std_bin_hori_img = rotate_horizontal(std_bin_img, std_cnt)
    std_hori_img = rotate_horizontal(std_img, std_cnt)
    var_bin_hori_img = rotate_horizontal(var_bin_img, var_cnt)
    var_hori_img = rotate_horizontal(var_img, var_cnt)
    std_max_height, std_max_width = get_max_size(std_bin_hori_img)
    var_max_height, var_max_width = get_max_size(var_bin_hori_img)
    std_crop_size = (int(std_max_width) * size_error, int(std_max_height) * size_error)
    var_crop_size = (int(var_max_width) * size_error, int(var_max_height) * size_error)
    std_bin_crop_img = crop_center(std_bin_hori_img, std_crop_size)
    std_crop_img = crop_center(std_hori_img, std_crop_size)
    var_bin_crop_img = crop_center(var_bin_hori_img, var_crop_size)
    var_crop_img = crop_center(var_hori_img, var_crop_size)
    y_scale = std_max_height / var_max_height
    std_width = std_bin_crop_img.shape[1]
    var_width = var_bin_crop_img.shape[1]
    x_scale = std_width / var_width
    var_bin_resized_img = cv2.resize(
        var_bin_crop_img, dsize=None, fx=x_scale, fy=y_scale
    )
    var_resized_img = cv2.resize(var_crop_img, dsize=None, fx=x_scale, fy=y_scale)
    std_crop_height = std_bin_crop_img.shape[0]
    var_crop_height = var_bin_resized_img.shape[0]
    if var_crop_height > std_crop_height:
        var_resized_width = var_bin_resized_img.shape[1]
        input_var_img = crop_center(
            var_bin_resized_img, (var_resized_width, std_crop_height)
        )
        var_color_img = crop_center(
            var_resized_img, (var_resized_width, std_crop_height)
        )
    elif var_crop_height < std_crop_height:
        diff_height = std_crop_height - var_crop_height
        top = diff_height // 2
        bottom = diff_height - top
        input_var_img = cv2.copyMakeBorder(
            var_bin_resized_img, top, bottom, 0, 0, cv2.BORDER_CONSTANT
        )
        var_color_img = cv2.copyMakeBorder(
            var_resized_img, top, bottom, 0, 0, cv2.BORDER_CONSTANT
        )
    else:
        input_var_img = var_bin_resized_img
        var_color_img = var_resized_img
    transhape = align_shape_horizontal(
        std_bin_crop_img, input_var_img, width_range, slide_range
    )
    output_var_img = transhape(var_color_img)
    return std_crop_img, output_var_img
