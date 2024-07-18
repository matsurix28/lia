def get_unique_px(df):
    """Get unique value pixel.

    Parameters
    ----------
    df : pandas.DataFrame
        {"blue", "green", "red", "fvfm"}

    Returns
    -------
    uniq : pands.DataFrame
        Unique data frame. ["blue", "green", "red", "fvfm"]
    """
    uniq = df[["blue", "green", "red", "fvfm"]].drop_duplicates()
    return uniq
