import os
import sys
import time

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia import ExtractFvFm, ExtractLeaf


def main():
    test_extract_fvfm()


def test_extract_leaf():
    e = ExtractLeaf()
    e.set_param(thresh=60)
    e.get_by_thresh("example/input_data/1-F.bmp")


def test_extract_fvfm():
    e = ExtractFvFm()
    e.get_list("example/input_data/1-F.bmp")


if __name__ == "__main__":
    main()
