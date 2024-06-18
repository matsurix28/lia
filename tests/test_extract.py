import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.core.extract import ExtractLeaf


def main():
    test_extr_fvfm()


def test_receive_kwargs():
    extr = ExtractLeaf()
    extr.get_by_color("example/input_data/1-L.JPG")
    print("owari")


def test_extr_fvfm():
    extr = ExtractLeaf()
    extr.set_param(thresh=60)
    extr.get_by_thresh("example/input_data/1-F.bmp")
    print("owari")


if __name__ == "__main__":
    main()
