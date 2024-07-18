from lia.align.overlap import (
    SCALING_FACTOR,
    SIZE_ERROR,
    SLIDE_RANGE,
    adjust_shape_horizontal,
)
from lia.core.base import ImageCore


class AlignLeaf(ImageCore):
    """Scale and move the leaf so that they just overlap.

    Attributes
    ----------
    size_error : float
        Error in approximate contour of leaf.
    scaling_factor : int
        Pecentage to be scaled.
    slide_range : int
        Percentage to move.
    """

    def __init__(self):
        super().__init__()
        # Set default value.
        self.size_error = SIZE_ERROR
        self.scaling_factor = SCALING_FACTOR
        self.slide_range = SLIDE_RANGE

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
        super().set_param(**kwargs)

    def horizontal(self, std_input, var_input, std_cnt, var_cnt):
        """Scale and move the leaf horizontally so that they just overlap.

        Parameters
        ----------
        std_input : str or numpy.ndarray
            Input standard image or its path.
        var_input : srt or numpy.ndarray
            Input image to be scaled or its path.
        std_cnt : [[[int, int]], ...]
            Contours of std_input.
        var_cnt : [[[int, int], ...]]
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
        std_img = self.input_img(std_input)
        var_img = self.input_img(var_input)
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
