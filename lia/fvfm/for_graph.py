from plotly.subplots import make_subplots

from lia.dataframe.add import add_hue
from lia.fvfm.to_dataframe import to_bgr_and_fvfm_dataframe
from lia.fvfm.unique_px import get_unique_px
from lia.graph.color import to_graph_rgb
from lia.graph.make_graph import make_2dscatter, make_3dscatter


def input_data_for_graph(px, fvfm_value):
    """Prepare input data for graphing.

    Parameters
    ----------
    px : [[int, int, int], ...]
        List of BGR values per pixel.
    fvfm_value : [int, ...]
        Fv/Fm value corresponding to each pixel.

    Returns
    -------
    blue : [int, ...]
        List of blue value.
    green : [int, ...]
        List of green value.
    red : [int, ...]
        List of red value.
    color : [str, ...]
        List of color for graph.
    hue : [int, ...]
        List of hue value.
    fvfm : [int, ...]
        List of Fv/Fm value.
    """
    # Convert to data frame to remove duplicates.
    df = to_bgr_and_fvfm_dataframe(px, fvfm_value)
    uniq_df = get_unique_px(df)
    df_hue = add_hue(uniq_df)
    blue = df_hue["blue"]
    green = df_hue["green"]
    red = df_hue["red"]
    hue = df_hue["hue"]
    fvfm = df_hue["fvfm"]
    color_list = df_hue[["red", "green", "blue"]].to_numpy().tolist()
    color = to_graph_rgb(color_list)
    return blue, green, red, color, hue, fvfm


def draw_graph(blue, green, red, color, hue, fvfm, name=None, fvfm_range=None):
    """Draw graphs of leaf color and Fv/Fm value.

    Parameters
    ----------
    blue : [int, ...]
        Blue, X axis.
    green : [int, ...]
        Green, Y axis.
    red : [int, ...]
        Red, Z axis.
    color : [[int, int, int], ...]
        List of BGR color.
    hue : [int, ...]
        Hue.
    fvfm : [float, ...]
        Fv/Fm value.
    name : str, optional
        Sample name.
    fvfm_range : (int, int), optional
        Range of Fv/Fm scalebar.

    Returns
    -------
    fig_fvfm2d : plotly.graph_objects.Figure
        2D scatter figure of Hue and Fv/Fm.
    fig_color3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color.
    fig_fvfm3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color and Fv/Fm value.
    """
    fvfm2d_figure_name = "2D scatter of Hue and Fv/Fm value " + name
    fig_fvfm2d = make_2dscatter(
        x=hue,
        y=fvfm,
        xaxis_title="Hue",
        yaxis_title="Fv/Fm",
        fig_title=fvfm2d_figure_name,
        marker_color=color,
    )
    color3d_figure_name = "3D scatter of leaf color " + name
    fig_color3d = make_3dscatter(
        x=blue,
        y=green,
        z=red,
        xaxis_title="Blue",
        yaxis_title="Green",
        zaxis_title="Red",
        xaxis_range=(0, 255),
        yaxis_range=(0, 255),
        zaxis_range=(0, 255),
        fig_title=color3d_figure_name,
        marker_color=color,
    )
    fvfm3d_figure_name = "3D scatter of leaf color and Fv/Fm value " + name
    fig_fvfm3d = make_3dscatter(
        x=blue,
        y=green,
        z=red,
        xaxis_title="Blue",
        yaxis_title="Green",
        zaxis_title="Red",
        xaxis_range=(0, 255),
        yaxis_range=(0, 255),
        zaxis_range=(0, 255),
        fig_title=fvfm3d_figure_name,
        marker_color=fvfm,
        colorbar_title="Fv/Fm",
        colorbar_range=fvfm_range,
    )
    return fig_fvfm2d, fig_color3d, fig_fvfm3d


def multi_graph(fig_fvfm2d, fig_color3d, fig_fvfm3d):
    """Summarize the three graphs.

    Parameters
    ----------
    fig_fvfm2d : plotly.graph_objects.Figure
        2D scatter figure of Hue and Fv/Fm.
    fig_color3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color.
    fig_fvfm3d : plotly.graph_objects.Figure
        3D scatter figure of leaf color and Fv/Fm value.

    Returns
    -------
    fig_multi : plotly.graph_objects.Figure
        Summarized graph.
    """
    fig_multi = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "xy"}, {"type": "scatter3d"}, {"type": "scatter3d"}]],
        subplot_titles=["Hue and Fv/Fm", "Leaf color", "Leaf color and Fv/Fm"],
    )
    fig_multi.add_trace(fig_fvfm2d["data"][0], row=1, col=1)
    fig_multi.add_trace(fig_color3d["data"][0], row=1, col=2)
    fig_multi.add_trace(fig_fvfm3d["data"][0], row=1, col=3)
    scene = {
        "xaxis": {"title": "Blue", "range": [0, 255]},
        "yaxis": {"title": "Green", "range": [0, 255]},
        "zaxis": {"title": "Red", "range": [0, 255]},
        "aspectratio": {"x": 1, "y": 1, "z": 1},
    }
    fig_multi.update_layout(
        showlegend=False,
        xaxis={"title": "Hue"},
        yaxis={"title": "Fv/Fm"},
        scene=scene,
        scene2=scene,
    )
    return fig_multi
