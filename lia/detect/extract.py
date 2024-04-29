from lia.detect import extract_leaf_by_color, extract_leaf_by_thresh

from lia.basic.get.consts import (
    MIN_CNTS_RATIO,
    DIFF_ELLIPSE_SIZE,
    ERROR_ELLIPSE,
    THRESH,
    BLANK_RATIO,
    NOISE_RATIO_THRESH,
    CANNY_THRESH1,
    CANNY_THRESH2,
    NOISE_THRESH,
    LEAF_COLOR_FORMAT,
    LEAF_COLOR_LOWER,
    LEAF_COLOR_UPPER,
)


class ExtractLeaf:
    def __init__(self):
        self.min_cnts_ratio = MIN_CNTS_RATIO
        self.diff_ellipse_size = DIFF_ELLIPSE_SIZE
        self.error_ellipse = ERROR_ELLIPSE
        self.thresh = THRESH
        self.blank_ratio = BLANK_RATIO
        self.noise_ratio_thresh = NOISE_RATIO_THRESH
        self.canny_thresh1 = CANNY_THRESH1
        self.canny_thresh2 = CANNY_THRESH2
        self.noise_thresh = NOISE_THRESH
        self.leaf_color_format = LEAF_COLOR_FORMAT
        self.leaf_color_lower = LEAF_COLOR_LOWER
        self.leaf_color_upper = LEAF_COLOR_UPPER

    def set_param(self, **kwargs):
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

    def by_thresh():
        pass

    def by_color():
        pass
