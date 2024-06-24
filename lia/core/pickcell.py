import os

from lia.core.base import ImageCore


class Pickcell(ImageCore):
    def __init__(self):
        self.num_cpu = os.cpu_count()
