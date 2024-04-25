import cv2
import os
import sys
try:
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_center_object import get_center_object
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from lia.detect.get_cnts import get_cnts
    from lia.detect.get_center_object import get_center_object

def main():
    img = cv2.imread('example/input_data/1-L.JPG')
    cnts = debug_get_cnts(img)
    try:
        center = get_center_object(img, cnts)
    except Exception as e:
        print(e)
    print('saigo')

def debug_get_cnts(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
    return get_cnts(thr)
    

if __name__ == '__main__':
    main()
