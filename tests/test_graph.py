import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia.graph.color import to_graph_rgb
from lia.graph.make_graph import make_2dscatter, make_3dscatter


def main():
    test_3d()


def test_3d():
    x = [2, 3, 4, 5]
    y = [12, 24, 56, 67]
    z = [33, 32, 51, 2]
    value = [40, 30, 80, 50]
    col = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255]]
    graph_col = to_graph_rgb(col)
    color = ["rgb(255, 0,0)", "rgb(0,255,0)", "rgb(0,0,255)", "rgb(255,0,255)"]
    fig = make_3dscatter(
        x,
        y,
        z,
        xaxis_title="x dayo",
        yaxis_title="y desu",
        zaxis_title="zzz",
        xaxis_range=(0, 100),
        marker_size=5,
        marker_color=value,
        colorbar_title="baar",
        fig_title="figiiire",
        colorbar_range=(0, 100),
    )
    fig.show()


def test2d():
    x = [3, 4, 5]
    y = [44, 6, 12]
    value = [50, 20, 60]
    col = [[255, 0, 0], [255, 255, 0], [0, 0, 255]]
    graph_col = to_graph_rgb(col)
    fig = make_2dscatter(
        x,
        y,
        xaxis_title="xxx",
        yaxis_title="yyyyy",
        xaxis_range=(0, 100),
        marker_color=value,
        colorbar_title="ttt",
        colorbar_range=(0, 100),
    )
    fig.show()


def test_df():
    px = [[107, 196, 98], [20, 100, 200], [50, 30, 70]]
    fvfm = [40, 10, 90]
    import pandas as pd

    df = pd.DataFrame(px, columns=["blue", "green", "red"])
    df["fvfm"] = fvfm
    from lia.dataframe.add import add_hue

    new_df = add_hue(df)
    print("owr")


if __name__ == "__main__":
    main()
