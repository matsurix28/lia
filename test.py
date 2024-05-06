import cv2


def save(img):
    cv2.imwrite("test.png", img)


img = cv2.imread("example/input_data/1-F.bmp")
save(img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img)
save(h)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
save(gray)
gray_inv = cv2.bitwise_not(gray)
save(gray_inv)
_, bin = cv2.threshold(gray_inv, 30, 255, cv2.THRESH_BINARY)
save(bin)
