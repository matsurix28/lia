import numpy as np


def search_closest_color(query_list, color_list, value_list=None):
    """Search closest color.

    Parameters
    ----------
    color_list : [[int, int, int], ...]
        List of standard color.
    query_list : [[int, int, int], ...]
        List of query.
    value_list : [int, ...], optional
        List of value.

    Returns
    -------
    color : [[int, int, int], ...]
        List of color.
    value : [int, ...], optional
        List of value.
    """
    color = []
    value = []
    if value_list is None:
        for query in query_list:
            idx = np.abs(color_list - query).sum(axis=1).argmin()
            color.append(color_list[idx])
        return color
    else:
        for query in query_list:
            idx = np.abs(color_list - query).sum(axis=1).argmin()
            color.append(color_list[idx])
            value.append(value_list[idx])
        return color, value
