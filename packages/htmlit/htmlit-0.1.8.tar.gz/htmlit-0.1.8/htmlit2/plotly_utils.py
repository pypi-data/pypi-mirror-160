import logging

import plotly
import plotly.graph_objs as go


def make_plotly_line(**kw):
    data = [
        go.Scatter(
            x=kw["x"],
            y=kw["y"],
        )
    ]
    layout = go.Layout(
        xaxis=dict(
            title=kw.get("x_label"),
        ),
        yaxis=dict(
            title=kw.get("y_label"),
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    return plotly.offline.plot(
        fig,
        config={"displayModeBar": False},
        output_type="div",
    )


log = logging.getLogger(__name__)
