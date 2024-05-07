import os
import sys

import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.basic.transform.rotate import rotate
from lia.detect import extract_leaf_by_thresh


def main():
    test_rotate()


def input_img():
    img = cv2.imread("example/input_data/rotate.bmp")
    return img


def test_rotate():
    img = input_img()
    cnts_list = extract_leaf_by_thresh(img)
    center, a, angle = cv2.fitEllipse(cnts_list[0])
    rotate(img, angle, center)


if __name__ == "__main__":
    main()
