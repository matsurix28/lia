import os

import cv2
import numpy as np

from lia import ExtractLeaf
from lia.align.overlap import (
    SCALING_FACTOR,
    SIZE_ERROR,
    SLIDE_RANGE,
    adjust_shape_horizontal,
)


class AlignLeaf:
    def __init__(self):
        # Set default value.
        self.size_error = SIZE_ERROR
        self.scaling_factor = SCALING_FACTOR
        self.slide_range = SLIDE_RANGE
        self.extract = ExtractLeaf()

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
            If input path is not image file.
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

    def set_param(self, **kwargs):
        """Set parameters.

        Parameters
        ----------
        size_error : float
            Error in approximate contour of leaf.
        scaling_factor : int
            Pecentage to be scaled.
        slide_range : int
            Percentage to move.
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
        self.extract.set_param(**kwargs)

    def horizontal(self, std_input, var_input, std_cnt=None, var_cnt=None):
        """Scale and move the leaf horizontally so that they just overlap.

        Parameters
        ----------
        std_input : str or numpy.ndarray
            Input standard image or its path.
        var_input : srt or numpy.ndarray
            Input image to be scaled or its path.
        std_cnt : [[[int, int]], ...], optional
            Contours of std_input.
        var_cnt : [[[int, int], ...]], optional
            Contours of var_inupt.

        Returns
        -------
        std_crop_img : numpy.ndarray
            Standard image cropped around leaf.
        var_align_img : numpy.ndarray
            Output adjusted image.

        Raises
        ------
        TypeError
            If input is not image.
        """
        if type(std_input) == str:
            std_img = self.__input_img(std_input)
        elif type(std_input) == np.ndarray:
            std_img = std_input
        else:
            raise TypeError("Please enter path or image in ndarray format.")
        if type(var_input) == str:
            var_img = self.__input_img(var_input)
        elif type(var_input) == np.ndarray:
            var_img = var_input
        else:
            raise TypeError("Please enter path or image in ndarray format.")
        if std_cnt is None:
            _, std_cnt = self.extract(std_img)
        if var_cnt is None:
            _, var_cnt = self.extract(var_img)
        std_crop_img, var_align_img = adjust_shape_horizontal(
            std_img,
            var_img,
            std_cnt,
            var_cnt,
            self.size_error,
            self.scaling_factor,
            self.slide_range,
        )
        return std_crop_img, var_align_img
