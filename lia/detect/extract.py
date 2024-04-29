import os

import cv2
import numpy as np

from lia.basic.get.consts import (
    BEYOND_ERROR_ELLIPSE,
    BLANK_RATIO,
    CANNY_THRESH1,
    CANNY_THRESH2,
    DIFF_ELLIPSE_SIZE,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
    MIN_CNTS_RATIO,
    NOISE_RATIO_THRESH,
    NOISE_THRESH,
    THRESH,
)
from lia.detect import extract_leaf_by_color, extract_leaf_by_thresh


class ExtractLeaf:
    def __init__(self):
        # Set default value
        self.min_cnts_ratio = MIN_CNTS_RATIO
        self.diff_ellipse_size = DIFF_ELLIPSE_SIZE
        self.beyond_error_ellipse = BEYOND_ERROR_ELLIPSE
        self.thresh = THRESH
        self.blank_ratio = BLANK_RATIO
        self.noise_ratio_thresh = NOISE_RATIO_THRESH
        self.canny_thresh1 = CANNY_THRESH1
        self.canny_thresh2 = CANNY_THRESH2
        self.noise_thresh = NOISE_THRESH
        self.leaf_color_format = LEAF_COLOR_FORMAT
        self.leaf_color_lower = LEAF_COLOR_LOWER
        self.leaf_color_upper = LEAF_COLOR_UPPER

    def __draw_cnts(self, img, cnts):
        """Draw contours.

        Parameters
        ----------
        img : numpy.ndarray
            Input color image.
        cnts : [[[int, int]], ...]
            List of ontours.

        Returns
        -------
        [numpy.ndarray]
            Images with contours drawn.
        """
        imgs = []
        for cnt in cnts:
            res_img = img.copy()
            cv2.drawContours(res_img, [cnt], -1, (0, 0, 255), 3)
            imgs.append(res_img)
        return imgs

    def __input_img(self, input_path):
        if os.path.isfile(input_path):
            img = cv2.imread(input_path)
            if not isinstance(img, np.ndarray):
                raise TypeError(f"'{input_path}' is not an image file")
            else:
                self.img_name = os.path.splitext(os.path.basename(input_path))[0]
                return img
        else:
            raise ValueError(f"Cannot access '{input_path}': No such file or directory")

    def by_thresh(self, input_path):
        img = self.__input_img(input_path)
        leaf_cnt_candidates = extract_leaf_by_thresh(
            img,
            self.thresh,
            self.blank_ratio,
            self.noise_ratio_thresh,
            self.min_cnts_ratio,
            self.canny_thresh1,
            self.canny_thresh2,
            self.noise_ratio_thresh,
        )
        leaf_cnt_imgs = self.__draw_cnts(img, leaf_cnt_candidates)
        return leaf_cnt_imgs, leaf_cnt_candidates

    def by_color(self, input_path):
        img = self.__input_img(input_path)
        leaf_cnt = extract_leaf_by_color(
            img,
            self.leaf_color_lower,
            self.leaf_color_upper,
            self.leaf_color_format,
            self.min_cnts_ratio,
        )
        leaf_cnt_img = self.__draw_cnts(img, [leaf_cnt])
        return leaf_cnt_img, leaf_cnt

    def set_param(self, **kwargs):
        """Set parameter.

        Parameters
        ----------
        min_ratio : int
            Minimum area ratio (min_area = area / min_ratio).
        diff_ellipse_size : int
            Tolerance for difference between approximate ellipse and contour.
        beyond_error_ellipse : int
            Percentage of approximate ellipses that extend beyond the image.
        thresh : int
            Threshold to detect contours.
        blcnk_ratio : int
            Max ratio of blank area.
        noise_ratio_thresh : int
            Threshold of noise contours.
        canny_thresh1 : int
            Threshold 1 for canny.
        canny_thresh2 : int
            Threshold 2 for canny.
        noise_thresh : int
            Threshold for contours of noise.
        leaf_color_format : str
            Color format, HSV or RGB.
        leaf_color_lower : (int, int, int)
            Lower of color range.
        leaf_color_upper : (int, int, int)
            Upper of color range.
        """
        for key, value in kwargs.items():
            key_exist_cmd = f"is_key = self.{key})"
            try:
                exec(key_exist_cmd)
            except:
                continue
            if type(value) == str:
                exec_cmd = f"self.{key} = '{value}'"
            elif type(value) == int:
                exec_cmd = f"self.{key} = {value}"
            exec(exec_cmd)
