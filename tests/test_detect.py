import os
import sys

import cv2

try:
    from lia.detect.evaluate_noise import evaluate_noise
    from lia.detect.extract_leaf import extract_leaf
    from lia.detect.get_center_object import get_center_object
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_diff_ellipse import get_diff_ellipse
    from lia.detect.sort_hsv_cnts import sort_hsv_cnts
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from lia.detect.evaluate_noise import evaluate_noise
    from lia.detect.extract_leaf import extract_leaf
    from lia.detect.get_center_object import get_center_object
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_diff_ellipse import get_diff_ellipse
    from lia.detect.sort_hsv_cnts import sort_hsv_cnts


def main():
    debug_extr_leaf()
    print("finish")


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
    num_noise, noise_ratio = evaluate_noise(img_gray)
    return num_noise, noise_ratio


def debug_sort_hsv_cnts():
    img = input_img()
    try:
        sorted_cnts_list = sort_hsv_cnts(img)
    except Exception as e:
        print(e)
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
    leaf_candidate = extract_leaf(img)
    return leaf_candidate


def input_img():
    img = cv2.imread("example/input_data/1-L.JPG")
    return img


if __name__ == "__main__":
    main()
