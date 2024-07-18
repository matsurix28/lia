import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.basic.get.size import get_max_size
from lia.basic.transform.crop import crop_center, crop_left
from lia.basic.transform.rotation import rotate, rotate_horizontal
from lia.basic.transform.slide import slide_horizontal
from lia.detect import extract_leaf_by_thresh


def main():
    test_crop_left()


def input_img():
    img = cv2.imread("example/input_data/1-F.bmp")
    return img


def test_crop_left():
    img = input_img()
    cr = crop_left(img, 200)


def test_slide():
    img = input_img()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(img_gray, 30, 255, cv2.THRESH_BINARY)
    slide_img = slide_horizontal(bin, -40)


def test_crop():
    img = input_img()
    size = (400, 100)
    crop_center(img, size, pos_x=100)


def test_max_size():
    img = input_img()
    cnts_list = extract_leaf_by_thresh(img)
    img_bin = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(img_bin, cnts_list, 0, 255, -1)
    get_max_size(img_bin)


def test_rotate():
    img = input_img()
    cnts_list = extract_leaf_by_thresh(img)
    center, a, angle = cv2.fitEllipse(cnts_list[0])
    rotate(img, angle, center)


def test_rotate_horizontal():
    img = input_img()
    cnts_list = extract_leaf_by_thresh(img)
    rotate_horizontal(img, cnts_list[0])


if __name__ == "__main__":
    main()
