from lia.color.search import closest_color


def search_fvfm(leaf_color, fvfm_color, fvfm_list):
    """Search closest fvfm value.

    Parameters
    ----------
    leaf_color : [[int, int, int], ...]
        Array of leaf color.
    fvfm_color : [[int, int, int], ...]
        Array of Fv/Fm color.
    fvfm_list : [int, ...]
        List of Fv/Fm value.

    Returns
    -------
    fvfm : [int, ...]
        Fv/Fm value corresponding to leaf color

    Raises
    ------
    ValueError
        Sizes differ.
    """
    if leaf_color.shape != fvfm_color.shape:
        raise ValueError("Sizes differ.")
    _, fvfm = closest_color(fvfm_color, leaf_color, fvfm_list)
    return fvfm
