import os
import sys

import cv2
import numpy as np

try:
    from lia.basic.get_hsv_cnts import get_hsv_cnts
    from lia.basic.get_noise import get_noise
    from lia.detect.detect_leaf import extrac_leaf_by_thresh
    from lia.detect.extract_leaf_bycolor import extract_color
    from lia.detect.get_center_object import get_center_object
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_diff_ellipse import get_diff_ellipse
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import lia
    from lia.basic.get import get_cnts_white_background
    from lia.detect.detect_leaf import extract_leaf_by_thresh


def main():
    debug_extr()
    print("finish")


def debug_extr_color():
    img = input_img()
    min = (30, 50, 50)
    max = (90, 255, 255)
    cnt = extract_color(img, min, max, color_format="hsv")
    cv2.drawContours(img, [cnt], 0, (255, 0, 0), 5)
    cv2.imwrite("tests/output/color_cnt.png", img)


def debug_get_cnts():
    img = input_img()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
    return get_cnts(thr)


def debug_center_object():
    img = input_img()
    cnts = debug_get_cnts()
    center = get_center_object(img, cnts)
    return cnts


def debug_evaluate_noise():
    img = input_img()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    num_noise, noise_ratio = get_noise(img_gray)
    return num_noise, noise_ratio


def debug_sort_hsv_cnts():
    img = input_img()
    try:
        sorted_cnts_list = get_hsv_cnts(img)
    except Exception as e:
        print(e)
    print(sorted_cnts_list)
    return sorted_cnts_list


def debug_diff_ellipse():
    img = input_img()
    cnts = debug_get_cnts()
    diff_area_list = []
    for cnt in cnts:
        try:
            diff_area = get_diff_ellipse(img, cnt)
        except Exception as e:
            print(e)
        else:
            diff_area_list.append(diff_area)
    return diff_area_list


def debug_extr_leaf():
    img = input_img()
    leaf_candidate = extrac_leaf_by_thresh(img)
    return leaf_candidate


def debug_extr():
    img = cv2.imread("example/input_data/1-L.JPG")
    leaf_candidates = extract_leaf_by_thresh(img)
    return leaf_candidates


def debug_extr_white_bg():
    img = cv2.imread("example/input_data/1-L.JPG")
    cnts_list = get_cnts_white_background(img)
    return cnts_list


def input_img():
    img = cv2.imread("example/input_data/1-L.JPG")
    return img


if __name__ == "__main__":
    main()
