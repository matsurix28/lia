import os

import cv2
import numpy as np

from lia.basic.evaluate._consts import CANNY_THRESH1, CANNY_THRESH2, NOISE_THRESH
from lia.basic.get._consts import (
    BEYOND_ERROR_ELLIPSE,
    BLANK_RATIO,
    DIFF_ELLIPSE_SIZE,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
    MIN_CNTS_RATIO,
    NOISE_RATIO_THRESH,
    THRESH,
    WHITE_BG_THRESH,
)
from lia.detect import extract_leaf_by_color, extract_leaf_by_thresh
from lia.detect.detect_fvfm import BAR_AREA_RATIO, WHITE_INV_THRESH, get_fvfm_list


class ExtractLeaf:
    """Extract leaf contours from image."""

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
        self.white_bg_thresh = WHITE_BG_THRESH

    def __draw_cnts_area(self, img, cnt):
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
        mask = np.zeros(img.shape, np.uint8)
        cv2.drawContours(mask, [cnt], -1, (255, 255, 255), -1)
        res_img = cv2.bitwise_and(img, mask)
        return res_img

    def __input_img(self, input_path):
        """Input image by cv2 format.

        Parameters
        ----------
        input_path : str
            Input image path.

        Returns
        -------
        img : numpy.ndarray
            cv2 format image.

        Raises
        ------
        TypeError
            if input is not image file.
        ValueError
            No such file.
        """
        if os.path.isfile(input_path):
            img = cv2.imread(input_path)
            if not isinstance(img, np.ndarray):
                raise TypeError(f"'{input_path}' is not an image file")
            else:
                self.img_name = os.path.splitext(os.path.basename(input_path))[0]
                return img
        else:
            raise ValueError(f"Cannot access '{input_path}': No such file or directory")

    def get_by_thresh(self, input_path):
        """Extract leaf by detecting contours.

        Parameters
        ----------
        input_path : str
            Input image path.

        Returns
        -------
        leaf_cnt_imgs : [numpy.ndarray, ...]
            List of images depicting the detected leaf contour candidates.
        leaf_cnt_candidates : [(array[[[int, int]], ...], ...), ...]
            Contours list of leaf candidates.
        """
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
            self.diff_ellipse_size,
            self.beyond_error_ellipse,
            self.white_bg_thresh,
        )
        leaf_cnt_imgs = []
        for cnt in leaf_cnt_candidates:
            leaf_img = self.__draw_cnts_area(img, cnt)
            leaf_cnt_imgs.append(leaf_img)
        # leaf_cnt_imgs = self.__draw_cnts_area(img, leaf_cnt_candidates)
        return leaf_cnt_imgs, leaf_cnt_candidates

    def get_by_color(self, input_path):
        """Extract leaf by color range.

        Parameters
        ----------
        input_path : str
            Input image path.

        Returns
        -------
        leaf_cnt_img : numpy.ndarray
            Image of a leaf outline drawn.
        leaf_cnt : (array[[[int, int]],...])
            Leaf contours.
        """
        img = self.__input_img(input_path)
        leaf_cnt = extract_leaf_by_color(
            img,
            self.leaf_color_lower,
            self.leaf_color_upper,
            self.leaf_color_format,
            self.min_cnts_ratio,
        )
        leaf_cnt_img = self.__draw_cnts_area(img, leaf_cnt)
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
            key_exist_cmd = f"is_key = self.{key}"
            try:
                exec(key_exist_cmd)
            except:
                continue
            if type(value) == str:
                exec_cmd = f"self.{key} = '{value}'"
            elif type(value) == int:
                exec_cmd = f"self.{key} = {value}"
            exec(exec_cmd)


class ExtractFvFm:
    def __init__(self) -> None:
        self.white_inv_thresh = WHITE_INV_THRESH
        self.bar_area_ratio = BAR_AREA_RATIO

    def __input_img(self, input_path):
        """Input image by cv2 format.

        Parameters
        ----------
        input_path : str
            Input image path.

        Returns
        -------
        img : numpy.ndarray
            cv2 format image.

        Raises
        ------
        TypeError
            if input is not image file.
        ValueError
            No such file.
        """
        if os.path.isfile(input_path):
            img = cv2.imread(input_path)
            if not isinstance(img, np.ndarray):
                raise TypeError(f"'{input_path}' is not an image file")
            else:
                self.img_name = os.path.splitext(os.path.basename(input_path))[0]
                return img
        else:
            raise ValueError(f"Cannot access '{input_path}': No such file or directory")

    def get_list(self, input_path):
        """Get list of Fv/Fm value and color.

        Parameters
        ----------
        input_path : str
            Path of input image.

        Returns
        -------
        fvfm_list : [[[int, int, int], int], ...]
            List of color and Fv/Fm value.
        """
        img = self.__input_img(input_path)
        fvfm_list = get_fvfm_list(img, self.white_inv_thresh, self.bar_area_ratio)
        return fvfm_list

    def set_param(self, **kwargs):
        """Set parameter.

        Parameters
        ----------
        white_inv_thresh : int
            Threshold of whtie background.
        bar_area_ratio : int
            Ratio of minimum bar size.
        """
        for key, value in kwargs.items():
            key_exist_cmd = f"is_key = self.{key}"
            try:
                exec(key_exist_cmd)
            except:
                continue
            if type(value) == str:
                exec_cmd = f"self.{key} = '{value}'"
            elif type(value) == int:
                exec_cmd = f"self.{key} = {value}"
            exec(exec_cmd)
