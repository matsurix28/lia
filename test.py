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


std_img = img.copy()
std_img = cv2.imread("example/input_data/1-L.JPG")
gray = cv2.cvtColor(std_img, cv2.COLOR_BGR2GRAY)
_, std_img = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
var_img = img.copy()
gray = cv2.cvtColor(var_img, cv2.COLOR_BGR2GRAY)
_, var_img = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)
if (not len(std_img.shape) == 2) or (not len(var_img.shape) == 2):
    print("booo")
else:
    print("yoi")

cv2.imwrite("test.png", std_img)
cv2.imwrite("test.png", var_img)
re_img = cv2.resize(std_img, dsize=(820, 560))
overlap = cv2.bitwise_and(re_img, var_img)
overnot = cv2.bitwise_not(re_img, var_img)
overxor = cv2.bitwise_xor(re_img, var_img)
overor = cv2.bitwise_or(re_img, var_img)
cv2.imwrite("test.png", overlap)
cv2.imwrite("test.png", overnot)
cv2.imwrite("test.png", overxor)
cv2.imwrite("test.png", overor)
