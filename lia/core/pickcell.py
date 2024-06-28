import os

from lia.core.base import ImageCore


class Pickcell(ImageCore):
    def __init__(self):
        self.num_cpu = os.cpu_count()

    def set_param(self, **kwargs):
        super().set_param(**kwargs)

    def pick(self, input_std, input_var, std_cnt):
        pass
