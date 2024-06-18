import cv2
import numpy as np

from lia.align.overlap import (
    asjust_shape_horizontal,
    SIZE_ERROR,
    SCALING_FACTOR,
    SLIDE_RANGE,
)
from lia.basic.get._consts import (
    MIN_CNTS_RATIO,
    DIFF_ELLIPSE_SIZE,
    BEYOND_ERROR_ELLIPSE,
    THRESH,
    BLANK_RATIO,
    NOISE_RATIO_THRESH,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
    WHITE_BG_THRESH,
)
from lia.basic.evaluate._consts import CANNY_THRESH1, CANNY_THRESH2, NOISE_THRESH


class AlignLeaf:
    def __init__(self):
        self.size_error = SIZE_ERROR
        self.scaling_factor = SCALING_FACTOR
        self.slide_range = SLIDE_RANGE
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

    def set_param(self, **kwargs):
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

    def horizontal(self, std_input, var_input, std_cnt=None, var_cnt=None):
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
            pass
