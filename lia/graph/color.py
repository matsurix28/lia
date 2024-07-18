def to_graph_rgb(rgb):
    """Convert RGB list to color information for graph.

    Parameters
    ----------
    rgb : [[int, int, int], ...]
        List of RGB value.

    Returns
    -------
    color : [str, ...]
        Marker color of graph.
    """
    color = [f"rgb({i[0]}, {i[1]}, {i[2]})" for i in rgb]
    return color
