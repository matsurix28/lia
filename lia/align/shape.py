import cv2

from lia.basic.transform.crop import crop


def align_shape_horizontal(std_img, var_img, width_range, pos_range):
    std_height, std_width = std_img.shape[:2]
    var_height, var_width = var_img.shape[:2]
    if not std_height == var_height:
        var_img = cv2.resize(var_img, dsize=(var_width, std_height))
    for i in range(-width_range, width_range, 1):
        fx = (100 + i) / 100
        resized_img = cv2.resize(var_img, dsize=None, fx=fx, fy=1)
        for pos in range(-pos_range, pos_range, 1):
            cropped_img = crop(
                resized_img,
            )
