import os
import sys
import time

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia import AlignLeaf, ExtractFvFm, ExtractLeaf, Graph, Pickcell


def main():
    test_graph()


def test_extract_leaf():
    e = ExtractLeaf()
    e.set_param(thresh=60)
    e.get_by_thresh("example/input_data/1-F.bmp")


def test_extract_fvfm():
    e = ExtractFvFm()
    e.get_list("example/input_data/1-F.bmp")


def test_pickcell():
    p = Pickcell()
    # p.set_param(thr1=200)
    img1 = cv2.imread("example/input_data/1-L.JPG")
    img1 = cv2.resize(img1, dsize=(500, 500))
    img2 = cv2.imread("example/input_data/1-F.bmp")
    img2 = cv2.resize(img2, dsize=(500, 500))
    col1, col2 = p.pick_color(img1, img2)
    print("owari")


def test_pickcell_fvfm():
    el = ExtractLeaf()
    ef = ExtractFvFm()
    leaf_imgs, leaf_cnts = el.get_by_thresh("example/input_data/1-L.JPG")
    fvfm_imgs, fvfm_cnts = el.get_by_thresh("example/input_data/1-F.bmp")
    fvfm_color_list, fvfm_value_list = ef.get_list("example/input_data/1-F.bmp")
    a = AlignLeaf()
    fvfm_img, leaf_img = a.horizontal(
        fvfm_imgs[0], leaf_imgs[0], fvfm_cnts[0], leaf_cnts[0]
    )
    p = Pickcell()
    p.pick_fvfm(leaf_img, fvfm_img, fvfm_color_list, fvfm_value_list)


def test_graph():
    el = ExtractLeaf()
    ef = ExtractFvFm()
    leaf_imgs, leaf_cnts = el.get_by_thresh("example/input_data/1-L.JPG")
    fvfm_imgs, fvfm_cnts = el.get_by_thresh("example/input_data/1-F.bmp")
    fvfm_color_list, fvfm_value_list = ef.get_list("example/input_data/1-F.bmp")
    a = AlignLeaf()
    fvfm_img, leaf_img = a.horizontal(
        fvfm_imgs[0], leaf_imgs[0], fvfm_cnts[0], leaf_cnts[0]
    )
    p = Pickcell()
    p.set_param(thr1=60, thr2=60)
    leaf_color, fvfm_color, fvfm_value = p.pick_fvfm(
        leaf_img, fvfm_img, fvfm_color_list, fvfm_value_list
    )
    g = Graph()
    fig_fvfm2d, fig_color3d, fig_fvfm3d, fig_multi = g.draw_fvfm(
        leaf_color, fvfm_value, "1no leaf"
    )
    fig_multi.show()
    print("owr")


if __name__ == "__main__":
    main()
