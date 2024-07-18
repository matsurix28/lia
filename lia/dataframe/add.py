from lia.color.convert import rgb2hsv


def add_hue(df):
    """Add hue column to dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing "red", "green", and "bLue" columns.

    Returns
    -------
    result : pandas.DataFrame
        DataFrame containing "hue" column.
    """

    def rgb2hue_dataframe(row):
        """Conver RGB of dataframe to HSV.

        Parameters
        ----------
        row : pandas.Series
            Row of dataframe.

        Returns
        -------
        hue : float
            Hue.
        """
        red = row["red"]
        green = row["green"]
        blue = row["blue"]
        hue, _, _ = rgb2hsv(red, green, blue)
        return hue

    result = df.assign(hue=lambda x: x.apply(rgb2hue_dataframe, axis=1))
    return result
