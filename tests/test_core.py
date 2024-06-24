import os
import sys
import time

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def main():
    # al = AlignLeaf()
    # al.horizontal("example/input_data/1-F.bmp", "example/input_data/test.png")
    start = time.time()
    import lia

    end = time.time()
    print(end - start)
    start = time.time()
    test()
    end = time.time()
    print(end - start)
    start = time.time()
    test()
    end = time.time()
    print(end - start)


def test():
    import easyocr


if __name__ == "__main__":
    main()
