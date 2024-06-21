import os

import cv2
import numpy as np


class ImageCore:
    def __input_img(self, input):
        """Input image by cv2 format.

        Parameters
        ----------
        input : numpy.ndarray or str
            Input image or its path.

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
        if type(input) == np.ndarray:
            return input
        elif type(input) == str:
            if os.path.isfile(input):
                img = cv2.imread(input)
                if type(img) != np.ndarray:
                    raise TypeError(f"'{input}' is not an image file.")
                else:
                    return img
            else:
                raise ValueError(f"Cannot access '{input}': No such file.")

    def __get_file_name(self, path):
        """Get file name.

        Parameters
        ----------
        path : str
            Path of file.

        Returns
        -------
        file_name : str
            File name.

        Raises
        ------
        ValueError
            If input is not file.
        """
        if os.path.isfile(path):
            file_name = os.path.splitext(os.path.basename(path))
            return file_name
        else:
            raise ValueError(f"'{path}' is not file.")
