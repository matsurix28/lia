import cv2


def save(img):
    cv2.imwrite("test.png", img)


img = cv2.imread("example/input_data/1-F.bmp")
hanten = cv2.bitwise_not(img)
save(hanten)
img_gray = cv2.cvtColor(hanten, cv2.COLOR_BGR2GRAY)
_, bin = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
len(cnts)
import os
import sys

sys.path.append(os.path.dirname(__file__))
from lia.basic.get import get_center_object

cnt = get_center_object(img, cnts)
len(cnt)
cv2.drawContours(img, [cnt], 0, (255, 0, 0), 5)
save(img)
