import cv2
import numpy as np


def rotate_horizontal(img, cnts):
    center, _, angle = cv2.fitEllipse(cnts)
    bin = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours


def rotate(img, angle, center):
    height, width = img.shape[:2]
    corners = np.array([(0, 0), (width, 0), (width, height), (0, height)])
    radius = np.sqrt(max(np.sum((center - corners) ** 2, axis=1)))
    frame = int(radius * 2)
    trans = cv2.getRotationMatrix2D(center, angle - 90, 1)
    trans[0][2] += radius - center[0]
    trans[1][2] += radius - center[1]
    rotated_img = cv2.warpAffine(img, trans, (frame, frame))
    return rotated_img
