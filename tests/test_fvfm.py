import os
import sys
import time

import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.detect.detect_fvfm import get_bar_area, read_fvfm_value
from lia.core.extract import ExtractFvFm


def main():
    test_extr_fvfm_leaf()


def input():
    img = cv2.imread("example/input_data/1-F.bmp")
    return img


def test_read_fvfm_value():
    img = input()
    read_fvfm_value(img)


def test_get_bar_area():
    img = input()
    get_bar_area(img)


def test_extr_fvfm_leaf():
    ex = ExtractFvFm()
    fvfm = ex.get_list("example/input_data/1-F.bmp")
    print(fvfm)


if __name__ == "__main__":
    main()
