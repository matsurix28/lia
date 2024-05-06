import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.detect.extract import ExtractLeaf


def main():
    test_extr_fvfm()


def test_receive_kwargs():
    extr = ExtractLeaf()
    extr.by_color("example/input_data/1-L.JPG")
    print("owari")


def test_extr_fvfm():
    extr = ExtractLeaf()
    extr.set_param(thresh=60)
    extr.by_thresh("example/input_data/1-L.JPG")
    print("owari")


if __name__ == "__main__":
    main()
