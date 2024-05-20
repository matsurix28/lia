import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.align.shape import align_shape_horizontal
from lia.basic.get.size import get_max_size
from lia.basic.transform.crop import crop_center
from lia.basic.transform.rotate import rotate_horizontal
from lia.detect import extract_leaf_by_thresh
from lia.detect.extract import ExtractLeaf


def main():
    leaf, fvfm, leaf_cnt, fvfm_cnt = extr()
    leaf = rotate_horizontal(leaf, leaf_cnt)
    fvfm = rotate_horizontal(fvfm, fvfm_cnt)
    leaf_max_height, max_width = get_max_size(leaf)
    fvfm_max_height, _ = get_max_size(fvfm)
    scale = fvfm_max_height / leaf_max_height
    leaf_re = cv2.resize(leaf, dsize=None, fx=1, fy=scale)
    fvfm_height = fvfm.shape[0]
    leaf_width = leaf_re.shape[1]
    leaf_cro = crop_center(leaf_re, (leaf_width, fvfm_height))
    transhape = align_shape_horizontal(fvfm, leaf_cro, 30, 20)
    leaf_img = cv2.imread("example/input_data/test.png")
    fvfm_img = cv2.imread("example/input_data/1-F.bmp")
    leaf_rotated = rotate_horizontal(leaf_img, leaf_cnt)
    fvfm_rotated = rotate_horizontal(fvfm_img, fvfm_cnt)
    leaf_re_img = cv2.resize(leaf_rotated, dsize=None, fx=1, fy=scale)
    leaf_cro_img = crop_center(leaf_re_img, (leaf_width, fvfm_height))
    ll = transhape(leaf_cro_img)
    img_over = cv2.addWeighted(src1=ll, alpha=1, src2=fvfm_rotated, beta=0.3, gamma=0)
    cv2.imwrite("test.png", img_over)
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
    return leaf, fvfm, leaf_cnts[0], fvfm_cnts[0]


if __name__ == "__main__":
    main()
