import os
from multiprocessing import Pool

import numpy as np

from lia.basic.transform.to_array import to_color_array
from lia.color.pickup import COLOR_THRESH1, COLOR_THRESH2, pickup_over_thresh
from lia.color.search import search_closest_color
from lia.core.base import ImageCore


class Pickcell(ImageCore):
    """Pick up pixels in overlapping areas in two images.

    Attributes
    ----------
    num_cpu : int
        Number of CPU.
    thr1 : int
        Threshold for color 1.
    thr2 : int
        Threshold for color 2.
    fvfm_color_list : [[int, int, int], ...]
        List of Fv/Fm scale color.
    fvfm_value_list : [int, ...]
        List of fv/Fm scale value.
    """

    def __init__(self):
        self.num_cpu = os.cpu_count()
        self.thr1 = COLOR_THRESH1
        self.thr2 = COLOR_THRESH2
        self.fvfm_color_list = None
        self.fvfm_value_list = None

    def set_param(self, **kwargs):
        """Set parameters.

        Parameters
        ----------
        thr1 : int
            Threshold for color 1.
        thr2 : int
            Threshold for color 2.
        fvfm_color_list : [[int, int, int], ...]
            List of Fv/Fm scale color.
        fvfm_value_list : [int, ...]
            List of fv/Fm scale value.
        """
        super().set_param(**kwargs)

    def get_color_array(self, input1, input2):
        """Reshape image to 2D array for multiprocess.

        Parameters
        ----------
        input1 : numpy.ndarray
            Input image 1.
        input2 : numpy.ndarray
            Input image 2.

        Returns
        -------
        px_colors : [[[int, int, int], [int, int, int]], ...]
            Array of color 1 and color 2.
        """
        img1 = self.input_img(input1)
        img2 = self.input_img(input2)
        color1 = to_color_array(img1)
        color2 = to_color_array(img2)
        colors1 = np.array_split(color1, self.num_cpu, axis=0)
        colors2 = np.array_split(color2, self.num_cpu, axis=0)
        px_colors = [[colors1[i], colors2[i]] for i in range(self.num_cpu)]
        return px_colors

    def pick_color(self, input1, input2):
        """Pick up color of pixels above threshold in each image.

        Parameters
        ----------
        input1 : numpy.ndarray or str
            Input image 1 or its path.
        input2 : numpy.ndarray or str
            Input image 2 or its path.

        Returns
        -------
        pick_color1 : [[int, int, int], ...]
            Array of colors 1 picked up.
        pick_color2 : [[int, int, int], ...]
            Array of colors 2 picked up.
        """
        px_colors = self.get_color_array(input1, input2)
        with Pool(self.num_cpu) as p:
            pick_colors = p.map(self.pool_func_pickup_color, px_colors)
        pick_color1 = [color for row in pick_colors for color in row[0]]
        pick_color2 = [color for row in pick_colors for color in row[1]]
        return pick_color1, pick_color2

    def pick_fvfm(self, leaf_img, fvfm_img, fvfm_color_list=None, fvfm_value_list=None):
        """Pick up color of pixels above threshold in each image and its Fv/Fm value.

        Parameters
        ----------
        leaf_img : numpy.ndarray or str
            Leaf image or its path.
        fvfm_img : numpy.ndarray or str
            Fv/Fm image or its path.
        fvfm_color_list : [[int, int, int], ...]
            List of Fv/Fm scale color.
        fvfm_value_list : [int, ...]
            List of Fv/Fm scale value.

        Returns
        -------
        leaf_color : [[int, int, int], ...]
            Array of leaf color picked up.
        fvfm_color : [[int, int, int], ...]
            Array of Fv/Fm scale color picked up.
        fvfm_value : [int, ...]
            Array of Fv/Fm scale value picked up.
        """
        if fvfm_color_list is not None:
            self.fvfm_color_list = fvfm_color_list
        if fvfm_value_list is not None:
            self.fvfm_value_list = fvfm_value_list
        px_colors = self.get_color_array(leaf_img, fvfm_img)
        with Pool(self.num_cpu) as p:
            results = p.map(self.pool_func_pickup_fvfm, px_colors)
        leaf_color = [color for row in results for color in row[0]]
        fvfm_color = [color for row in results for color in row[1]]
        fvfm_value = [value for row in results for value in row[2]]
        return leaf_color, fvfm_color, fvfm_value

    def pool_func_pickup_color(self, args):
        """Multiprocessing function. Pick up color of pixels above threshold in each image.

        Parameters
        ----------
        args : [[[int,int, int], [int, int, int]], ...]
            Array of color 1 and color 2.

        Returns
        -------
        Color1 : [[int, int, int], ...]
            Array of color 1 picked up.
        """
        color1, color2 = pickup_over_thresh(*args, self.thr1, self.thr2)
        return color1, color2

    def pool_func_pickup_fvfm(self, args):
        """Multiprocessing function. Pick up color of pixels above threshold in each image and its Fv/Fm value.

        Parameters
        ----------
        args : [[[int, int, int], [int, int, int]], ...]
            Array of leaf color 1 and Fv/Fm color 2.

        Returns
        -------
        leaf_color : [[int, int, int], ...]
            Array of leaf color picked up.
        fvfm_color : [[int, int, int], ...]
            Array of Fv/Fm color picked up.
        fvfm_value : [int, ...]
            Array of Fv/Fm value picked up.
        """
        leaf_color, fvfm_color = pickup_over_thresh(*args, self.thr1, self.thr2)
        _, fvfm_value = search_closest_color(
            fvfm_color, self.fvfm_color_list, self.fvfm_value_list
        )
        return leaf_color, fvfm_color, fvfm_value
