import cv2
import os
import sys
try:
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_center_object import get_center_object
    from lia.detect.evaluate_noise import evaluate_noise
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_center_object import get_center_object
    from lia.detect.evaluate_noise import evaluate_noise

def main():
    debug_evaluate_noise()

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

def input_img():
    img = cv2.imread('example/input_data/1-L.JPG')
    return img
    

if __name__ == '__main__':
    main()
