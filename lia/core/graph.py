from lia.fvfm.for_graph import draw_graph, input_data_for_graph, multi_graph


class Graph:
    """Draw graph."""

    def __init__(self):
        pass

    def draw_fvfm(self, px, fvfm_value, name=None, fvfm_range=None):
        """Draw graph of leaf color and Fv/Fm.

        Parameters
        ----------
        px : [[int, int, int], ...]
            List of BGR values per pixel.
        fvfm_value : [float, ...]
            Fv/Fm value corresponding to each pixel.
        name : str, optional
            Sample name
        fvfm_range : (int, int), optional
            Range of Fv/Fm scale bar.

        Returns
        -------
        fig_fvfm2d : plotly.graph_objects.Figure
            2D scatter figure of Hue and Fv/Fm.
        fig_color3d : plotly.graph_objects.Figure
            3D scatter figure of leaf color.
        fig_fvfm3d : plotly.graph_objects.Figure
            3D scatter figure of leaf color and Fv/Fm value.
        fig_multi : plotly.graph_objects.Figure
            Summary of above three graphs.
        """
        blue, green, red, color, hue, fvfm = input_data_for_graph(px, fvfm_value)
        fig_fvfm2d, fig_color3d, fig_fvfm3d = draw_graph(
            blue, green, red, color, hue, fvfm, name, fvfm_range
        )
        fig_multi = multi_graph(fig_fvfm2d, fig_color3d, fig_fvfm3d)
        return fig_fvfm2d, fig_color3d, fig_fvfm3d, fig_multi
