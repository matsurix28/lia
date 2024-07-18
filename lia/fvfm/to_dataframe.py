import pandas as pd


def to_bgr_and_fvfm_dataframe(px, fvfm_value):
    """Make data frame of BGR and Fv/Fm value.

    Parameters
    ----------
    px : [[int, int, int], ...]
        Array of color.
    fvfm_value : [int, ...]
        Array of Fv/Fm value.

    Returns
    -------
    df : pandas.DataFrame
        Data frame of color and Fv/Fm value.
    """
    df = pd.DataFrame(px, columns=["blue", "green", "red"])
    df["fvfm"] = fvfm_value
    return df
