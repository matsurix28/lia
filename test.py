import cv2


def save(img):
    cv2.imwrite("test.png", img)


img = cv2.imread("example/input_data/1-F.bmp")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
save(img_gray)
_, bin = cv2.threshold(img_gray, 30, 255, cv2.THRESH_BINARY)
save(bin)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
len(cnts)
cv2.drawContours(img, cnts, 0, (255, 0, 0), 5)
save(img)
