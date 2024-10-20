from lib.cmd_lib import get_command_line
from lib.utils_lib import save_plot_as_pdf

import plotly.graph_objects as go
import json, math

from typing import List
from palettable.cubehelix import Cubehelix
import numpy as np


def make_plot(height: int, width: int, loaded_experiments: dict, workers: List[int], colors,
              line_name_list_prod: List[str], output_plot_path: str):

    fig = go.Figure()
    shapes = ['circle', 'square', 'diamond']
    j = 5
    x_data = [w for w in workers]
    showlegend=True
    for i in range(len(line_name_list_prod)):
        y_data = [loaded_experiments['production'][line_name_list_prod[i]][f'worker{w}']['production_rate'] for w in workers]
        m = (y_data[1] - y_data[0])/(x_data[1] - x_data[0])
        y_new = m * np.array(x_data)
        fig.add_trace(go.Scatter(x=x_data, y=y_new,
                                 name=f'linear growth',
                                 showlegend=showlegend,
                                 mode='lines',
                                 line=dict(color='rgba(128, 128, 128, 0.15)', width=15, dash='solid'), ))

        showlegend=False

        fig.add_trace(go.Scatter(x=x_data, y=y_data,
                                 name=f'\u03C1<sub>APSG</sub> ({line_name_list_prod[i].upper()})',
                                 showlegend=True,
                                 mode='lines+markers',
                                 marker=dict(size=15, color=colors[j], symbol=shapes[i]),
                                 line=dict(color=colors[j], width=1, dash='solid'),))



        j += 3

    fig.update_layout(showlegend=True, height=height, width=width, title={
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=2, t=2, l=65, b=35),  # bargap=0.5,
                      legend=dict(font=dict(size=20), itemwidth=30, borderwidth=1.35,
                                  yanchor="bottom", y=0.73, xanchor="left", x=0.05,
                                  bgcolor='rgba(255,255,255, 1.0)'),
                      )

    fig.update_xaxes(title="number of simulators (n)", linewidth=1.5, linecolor='black', showline=True, showgrid=True, gridwidth=0.00001,
                     gridcolor='lightgrey', title_font={"size": 25}, tickfont=dict(size=18), mirror='ticks',
                     ticks="inside",
                     tickwidth=0, tickvals=[1, 64, 128, 256, 512, 1024, 2048], ticktext=[1, 64, 128, 256, 512, 1024, 2048])

    fig.update_yaxes(title="samples/sec", linewidth=1.5, linecolor='black', showline=True, showgrid=True, gridwidth=0.00001,
                     gridcolor='lightgrey', zeroline=True, zerolinecolor='lightgrey', zerolinewidth=0.00001,
                     showticklabels=True, #type="log", dtick=1,
                     title_font={"size": 25}, tickfont=dict(size=18), mirror='ticks', ticks="inside", tickwidth=0,
                     title_standoff=20)

    save_plot_as_pdf(fig, output_plot_path)


def main():
    experiments_data_path, output_plot_path = get_command_line()

    with open(experiments_data_path, 'r') as f:
        loaded_data = json.load(f)

    workers_used = [1, 64, 128, 256, 512, 1024, 2048]

    palette = Cubehelix.make(start=0.3, rotation=-0.5, n=16)
    colors = [f'rgb({c[0]},{c[1]},{c[2]})' for c in palette.colors]

    width_inch = 2.8 #3.54331
    dpi = 300

    height = 600
    width = math.ceil(width_inch * dpi)

    list_name_prod_sys = ['at', 'fcs', 'alma']

    make_plot(height, width, loaded_data, workers_used, colors, list_name_prod_sys, output_plot_path)


if __name__ == '__main__':
    main()