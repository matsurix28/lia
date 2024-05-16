import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.align.shape import align_shape_horizontal
from lia.basic.transform.rotate import rotate_horizontal
from lia.detect.extract import ExtractLeaf


def main():
    leaf, fvfm, leaf_cnt, fvfm_cnt = extr()
    leaf = rotate_horizontal(leaf, leaf_cnt)
    fvfm = rotate_horizontal(fvfm, fvfm_cnt)
    transhape = align_shape_horizontal(fvfm, leaf, 20, 20)
    leaf_img = cv2.imread("example/input_data/1-L.JPG")
    fvfm_img = cv2.imread("example/input_data/1-F.bmp")
    leaf_rotated = rotate_horizontal(leaf_img, leaf_cnt)
    fvfm_rotated = rotate_horizontal(fvfm_img, fvfm_cnt)
    ll = transhape(leaf_rotated)
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
