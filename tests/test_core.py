import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia import AlignLeaf


def main():
    al = AlignLeaf()
    al.horizontal("example/input_data/1-F.bmp", "example/input_data/1-L.JPG")


if __name__ == "__main__":
    main()
