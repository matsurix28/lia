import cv2
import os
import sys
try:
    from lia.detect.get_cnts import get_cnts
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from lia.detect.get_cnts import get_cnts

def main():
    test_get_cnts()

def test_get_cnts():
    img = cv2.imread('tests/img/1-L.JPG')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
    res = get_cnts(thr)
    assert type(res) == list
    

if __name__ == '__main__':
    main()
