from plotly import graph_objects as go

MARKER3D_SIZE = 1
MARKER2D_SIZE = 10


def make_3dscatter(
    x,
    y,
    z,
    xaxis_title="x",
    yaxis_title="y",
    zaxis_title="z",
    xaxis_range=None,
    yaxis_range=None,
    zaxis_range=None,
    fig_title=None,
    marker_size=MARKER3D_SIZE,
    marker_color=None,
    colorbar_title=None,
    colorbar_range=None,
):
    """Make 3d scatter graph.

    Parameters
    ----------
    x : list
        X axis data.
    y : list
        Y axis data.
    z : list
        Z axis data.
    xaxis_title : str, optional
        X axis title, by default "x"
    yaxis_title : str, optional
        Y axis title, by default "y"
    zaxis_title : str, optional
        Z axis title., by default "z"
    xaxis_range : (int, int), optional
        Range of X axis, by default range of x data.
    yaxis_range : (int, int), optional
        Range of Y axis., by default range of y data.
    zaxis_range : (int, int), optional
        Range of Z axis., by default range of z data.
    fig_title : str, optional
        Figure title., by default None
    marker_size : int, optional
        Size of marker.
    marker_color : list, optional
        Value of each plot., by default None
    colorbar_title : str, optional
        Value bar title., by default None
    colorbar_range : (int, int), optional
        Range of colorbar, by default (min value, max value)

    Returns
    -------
    fig : ploty.graph_objects
        3D scatter graph.
    """
    marker = {"size": marker_size}
    if marker_color is not None:
        if colorbar_range is None:
            cmin = None
            cmax = None
        else:
            cmin = colorbar_range[0]
            cmax = colorbar_range[1]
        marker.update(
            color=marker_color,
            cmin=cmin,
            cmax=cmax,
            colorbar={"title": colorbar_title},
            colorscale="Jet",
        )
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=marker,
            )
        ]
    )
    scene = {
        "xaxis": {"range": xaxis_range, "title": xaxis_title},
        "yaxis": {"range": yaxis_range, "title": yaxis_title},
        "zaxis": {"range": zaxis_range, "title": zaxis_title},
        "aspectratio": {"x": 1, "y": 1, "z": 1},
    }
    fig.update_layout(scene=scene, title=fig_title)
    return fig


def make_2dscatter(
    x,
    y,
    xaxis_title="x",
    yaxis_title="y",
    xaxis_range=None,
    yaxis_range=None,
    fig_title=None,
    marker_size=MARKER2D_SIZE,
    marker_color=None,
    colorbar_title=None,
    colorbar_range=None,
):
    """Make 2D scatter graph.

    Parameters
    ----------
    x : list
        X axis data.
    y : list
        Y axis data.
    xaxis_title : str, optional
        X axis title, by default "x"
    yaxis_title : str, optional
        Y axis title, by default "y"
    xaxis_range : (int, int), optional
        Range of X axis, by default None
    yaxis_range : (int, int), optional
        Range of Y axis, by default None
    fig_title : str, optional
        Figure title, by default None
    marker_size : int, optional
        Size of markers.
    marker_color : list, optional
        Value [int, ...] or color [[int, int, int], ...] of each plot, by default None
    colorbar_title : str, optional
        Colorbar title, by default None
    colorbar_range : (int, int), optional
        Range of colorbar, by default None

    Returns
    -------
    fig : plotly.graph_objects
        2D scatter graph.
    """
    marker = {"size": marker_size}
    if marker_color is not None:
        if colorbar_range is None:
            cmax = None
            cmin = None
        else:
            cmin = colorbar_range[0]
            cmax = colorbar_range[1]
        marker.update(
            color=marker_color,
            cmin=cmin,
            cmax=cmax,
            colorbar={"title": colorbar_title},
            colorscale="Jet",
        )
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="markers", marker=marker)])
    fig.update_layout(
        xaxis={"title": xaxis_title, "range": xaxis_range},
        yaxis={"title": yaxis_title, "range": yaxis_range},
        title=fig_title,
    )
    return fig
