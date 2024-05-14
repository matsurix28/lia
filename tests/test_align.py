import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.align.shape import align_shape_horizontal
from lia.detect.extract import ExtractLeaf


def main():
    leaf, fvfm = extr()
    align_shape_horizontal(fvfm, leaf, 20, 20)


def extr():
    e = ExtractLeaf()
    leaf_imgs, leaf_cnts = e.get_by_thresh("example/input_data/1-L.JPG")
    fvfm_imgs, fvfm_cnts = e.get_by_thresh("example/input_data/1-F.bmp")
    leaf_bin = np.zeros(leaf_imgs[0].shape[:2], dtype=np.uint8)
    fvfm_bin = np.zeros(fvfm_imgs[0].shape[:2], dtype=np.uint8)
    cv2.drawContours(leaf_bin, leaf_cnts, 0, 255, -1)
    cv2.drawContours(fvfm_bin, fvfm_cnts, 0, 255, -1)
    _, leaf = cv2.threshold(leaf_bin, 200, 255, cv2.THRESH_BINARY)
    _, fvfm = cv2.threshold(fvfm_bin, 200, 255, cv2.THRESH_BINARY)
    return leaf, fvfm


if __name__ == "__main__":
    main()
