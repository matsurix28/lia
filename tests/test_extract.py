import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.detect.extract import ExtractLeaf


def main():
    test_receive_kwargs()


def test_receive_kwargs():
    extr = ExtractLeaf()
    extr.set_param(nai=60, leaf_color_format="RGB", diff_ellipse_size=528)
    print("owari")


if __name__ == "__main__":
    main()
