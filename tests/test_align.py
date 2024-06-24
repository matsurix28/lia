import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.align.get_func import get_align_hori_func
from lia.align.overlap import adjust_shape_horizontal
from lia.basic.get.size import get_max_size
from lia.basic.transform.crop import crop_center
from lia.basic.transform.rotation import rotate_horizontal
from lia.core.extract import ExtractLeaf
from lia.detect import extract_leaf_by_thresh


def main():
    leaf, fvfm, leaf_cnt, fvfm_cnt = extr()
    fvfm_out, leaf_out = adjust_shape_horizontal(fvfm, leaf, fvfm_cnt, leaf_cnt)
    print("kk")


def main2():
    leaf, fvfm, leaf_cnt, fvfm_cnt = extr()
    leaf__color_img = cv2.imread("example/input_data/1-L.JPG")
    fvfm__color_img = cv2.imread("example/input_data/1-F.bmp")
    leaf = rotate_horizontal(leaf, leaf_cnt)
    fvfm = rotate_horizontal(fvfm, fvfm_cnt)
    leaf_rotated = rotate_horizontal(leaf__color_img, leaf_cnt)
    fvfm_rotated = rotate_horizontal(fvfm__color_img, fvfm_cnt)
    leaf_max_height, max_width = get_max_size(leaf)
    fvfm_max_height, _ = get_max_size(fvfm)
    height_scale = fvfm_max_height / leaf_max_height
    leaf_width = leaf.shape[1]
    fvfm_width = fvfm.shape[1]
    width_scale = fvfm_width / leaf_width
    leaf_re = cv2.resize(leaf, dsize=None, fx=width_scale, fy=height_scale)
    leaf_color_re = cv2.resize(
        leaf_rotated, dsize=None, fx=width_scale, fy=height_scale
    )
    # fvfm_height = fvfm.shape[0]
    # leaf_width = leaf_re.shape[1]
    # fvfm_width = fvfm.shape[1]
    # leaf_cro = crop_center(leaf_re, (leaf_width, fvfm_height))
    # wid_scale = fvfm_width / leaf_width
    # leaf_resize = cv2.resize(leaf_cro, dsize=None, fx=wid_scale, fy=1)
    leaf_re_height, leaf_re_width = leaf_re.shape[:2]
    fvfm_height = fvfm.shape[0]
    if leaf_re_height > fvfm_height:
        leaf_re = crop_center(leaf_re, (leaf_re_width, fvfm_height))
        leaf_color_re = crop_center(leaf_color_re, (leaf_re_width, fvfm_height))
    elif leaf_re_height < fvfm_height:
        diff_height = fvfm_height - leaf_re_height
        top = diff_height // 2
        bottom = diff_height - top
        leaf_re = cv2.copyMakeBorder(leaf_re, top, bottom, 0, 0, cv2.BORDER_CONSTANT)
        leaf_color_re = cv2.copyMakeBorder(
            leaf_color_re, top, bottom, 0, 0, cv2.BORDER_CONSTANT
        )
    transhape = get_align_hori_func(fvfm, leaf_re, 30, 20)
    leaf_color_after = transhape(leaf_color_re)
    img_over = cv2.addWeighted(
        src1=leaf_color_after, src2=fvfm_rotated, alpha=1, beta=0.3, gamma=0
    )
    # leaf_re_img = cv2.resize(leaf_rotated, dsize=None, fx=1, fy=scale)
    # leaf_cro_img = crop_center(leaf_re_img, (leaf_width, fvfm_height))
    # ll = transhape(leaf_cro_img)
    # img_over = cv2.addWeighted(src1=ll, alpha=1, src2=fvfm_rotated, beta=0.3, gamma=0)
    # cv2.imwrite("test.png", img_over)
    print("kkk")


def extr():
    e = ExtractLeaf()
    leaf_imgs, leaf_cnts = e.get_by_thresh("example/input_data/test.png")
    fvfm_imgs, fvfm_cnts = e.get_by_thresh("example/input_data/1-F.bmp")
    leaf_bin = np.zeros(leaf_imgs[0].shape[:2], dtype=np.uint8)
    fvfm_bin = np.zeros(fvfm_imgs[0].shape[:2], dtype=np.uint8)
    cv2.drawContours(leaf_bin, leaf_cnts, 0, 255, -1)
    cv2.drawContours(fvfm_bin, fvfm_cnts, 0, 255, -1)
    _, leaf = cv2.threshold(leaf_bin, 200, 255, cv2.THRESH_BINARY)
    _, fvfm = cv2.threshold(fvfm_bin, 200, 255, cv2.THRESH_BINARY)
    return leaf_imgs[0], fvfm_imgs[0], leaf_cnts[0], fvfm_cnts[0]


if __name__ == "__main__":
    main()
