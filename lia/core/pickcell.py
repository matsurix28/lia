import os
from multiprocessing import Pool

import numpy as np

from lia.basic.transform.to_array import to_color_array
from lia.color.pickup import COLOR_THRESH1, COLOR_THRESH2, pickup_over_thresh
from lia.core.base import ImageCore


class Pickcell(ImageCore):
    def __init__(self):
        self.num_cpu = os.cpu_count()
        self.thr1 = COLOR_THRESH1
        self.thr2 = COLOR_THRESH2

    def set_param(self, **kwargs):
        super().set_param(**kwargs)

    def get_color_array(self, input1, input2):
        img1 = self.input_img(input1)
        img2 = self.input_img(input2)
        color1 = to_color_array(img1)
        color2 = to_color_array(img2)
        colors1 = np.array_split(color1, self.num_cpu, axis=0)
        colors2 = np.array_split(color2, self.num_cpu, axis=0)
        px_colors = [[colors1[i], colors2[i]] for i in range(self.num_cpu)]
        return px_colors

    def pick_color(self, input1, input2):
        px_colors = self.get_color_array(input1, input2)
        with Pool(self.num_cpu) as p:
            pick_colors = p.map(self.pickup, px_colors)
        pick_color1 = [color[0] for color in pick_colors]
        pick_color2 = [color[1] for color in pick_colors]
        return pick_color1, pick_color2

    def pick_fvfm(self, leaf_img, fvfm_img):
        px_colors = self.get_color_array(leaf_img, fvfm_img)

    def pickup_color(self, args):
        color1, color2 = pickup_over_thresh(*args, self.thr1, self.thr2)
        return color1, color2

    def pickup_fvfm(self, args):
        leaf_color, fvfm_color = pickup_over_thresh(*args, self.thr1, self.thr2)
