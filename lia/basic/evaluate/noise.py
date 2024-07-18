import cv2

from ._consts import CANNY_THRESH1, CANNY_THRESH2, NOISE_THRESH


def get_noise(
    img, canny_thr1=CANNY_THRESH1, canny_thr2=CANNY_THRESH2, noise_thresh=NOISE_THRESH
):
    """Evaluate the amount of noise.

    Parameters
    ----------
    img : numpy.ndarray
        Input gray scale image.
    canny_thr1 : int (defautl: 100)
        Canny threshold 1.
    canny_thr2 : int (default: 200)
        Canny threshold 2.
    min_noise : int (default: 100)
        Minimum noise ratio (min_noise_area = area / min_noise).

    Returns
    -------
    num_noise : int
        Number of noise.
    noise_ratio : int
        Percent of noise.
    """
    img_canny = cv2.Canny(img, canny_thr1, canny_thr2)
    cnts_list, _ = cv2.findContours(
        img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    height, width = img.shape[:2]
    area = height * width
    max_noise = area / noise_thresh
    num_noise = len(list(filter(lambda x: cv2.contourArea(x) < max_noise, cnts_list)))
    noise_area_list = [cv2.contourArea(cnt) for cnt in cnts_list]
    noise_area = sum(noise_area_list)
    noise_ratio = int(noise_area / area * 100)
    return num_noise, noise_ratio
