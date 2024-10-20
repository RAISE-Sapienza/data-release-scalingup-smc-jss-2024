from lib.cmd_lib import get_command_line_plots
from lib.utils_lib import symmetric_logarithm, format_tick, save_plot_as_pdf

from palettable.cubehelix import Cubehelix

import plotly.graph_objects as go
import numpy as np

import math, json
from typing import List


def build_data_for_plot(loaded_data: dict, used_epsilon: List[float], used_delta: List[float]):
    builded_data = {'AA': dict(), 'EBGStop': dict(), 'saving': dict()}

    for delta in used_delta:
        builded_data['AA'][f'delta_{delta}'] = dict()
        builded_data['EBGStop'][f'delta_{delta}'] = dict()
        builded_data['saving'][f'delta_{delta}'] = dict()

        for epsilon in used_epsilon:
            aa_mean_sample = loaded_data[f'delta{delta}_epsilon{epsilon}']['AA']['samples']['mean']
            builded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}'] = dict()
            builded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}']['mean'] = aa_mean_sample
            builded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}']['error'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['AA']['samples']['error']
            builded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['AA']['samples']['values_list']

            ebgstop_mean_sample = loaded_data[f'delta{delta}_epsilon{epsilon}']['EBGStop']['samples']['mean']
            builded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}'] = dict()
            builded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}']['mean'] = ebgstop_mean_sample
            builded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}']['error'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['EBGStop']['samples']['error']
            builded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['EBGStop']['samples']['values_list']

            builded_data['saving'][f'delta_{delta}'][f'epsilon_{epsilon}'] = dict()
            builded_data['saving'][f'delta_{delta}'][f'epsilon_{epsilon}']['mean'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['relative_saving']['mean']
            builded_data['saving'][f'delta_{delta}'][f'epsilon_{epsilon}']['error'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['relative_saving']['error']
            builded_data['saving'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list'] = loaded_data[f'delta{delta}_epsilon{epsilon}']['relative_saving']['value_list']

    return builded_data


def make_plot(height_px, width_px, epsilon_used, used_delta, loaded_data, system_name, colors, output_data_folder_path: str):
    shapes = ['circle', 'square', 'diamond']
    fig = go.Figure()
    delta_notation = ['10<sup>-1</sup>', '5x10<sup>-2</sup>', '10<sup>-2</sup>']

    for epsilon in epsilon_used:
        color_idx = 5
        shape_idx = 0
        for delta in used_delta:
            showlegend = True
            sample_list_aa = loaded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list']
            sample_list_ebgstop = loaded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list']

            for i in range(len(sample_list_aa)):
                fig.add_trace(go.Scatter(
                    showlegend=True if showlegend and epsilon == 0.001 else False,
                    name=f'\u03b4={delta_notation[shape_idx]}',
                    x=[str(epsilon * 100)],
                    y=[symmetric_logarithm(min(sample_list_ebgstop[i], sample_list_aa[i]))],
                    mode='markers',
                    marker=dict(
                        size=11,
                        symbol=shapes[shape_idx],
                        color=colors[color_idx],
                    ),
                ))
                showlegend = False

            color_idx += 3
            shape_idx += 1

    for i in range(10):
        j = 5
        for delta in used_delta:
            random_seed_vals = []
            for epsilon in epsilon_used:
                sample_list_aa = loaded_data['AA'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list']
                sample_list_ebgstop = loaded_data['EBGStop'][f'delta_{delta}'][f'epsilon_{epsilon}']['value_list']
                random_seed_vals.append(symmetric_logarithm(min(sample_list_aa[i], sample_list_ebgstop[i])))

            fig.add_trace(go.Scatter(
                showlegend=False,
                visible=True,
                x=[str(epsilon * 100) for epsilon in epsilon_used],
                y=random_seed_vals,
                mode='lines',
                line=dict(
                    color=colors[j],
                    width=0.5,
                    dash='solid'
                )))
            j += 3


    fig.update_layout(showlegend=True, height=height_px, width=width_px, title={
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=0, t=10, l=10, b=0),
                      legend=dict(font=dict(size=20), itemwidth=30, borderwidth=1.35, y=0.90, x=0.75,
                                  bgcolor='rgba(255,255,255, 1)'),)

    fig.update_xaxes(linewidth=0.5, linecolor='black', showline=True, showgrid=True,
                     gridwidth=0.00001, zerolinewidth=0.00001,
                     gridcolor='lightgrey', title_font={"size": 25}, tickfont=dict(size=18), mirror='ticks',
                     ticks="inside",
                     tickvals=[str(epsilon * 100) for epsilon in epsilon_used],
                     ticktext=[str(epsilon * 100) for epsilon in epsilon_used])

    fig.update_yaxes(tickmode='array',
                     tickvals=symmetric_logarithm(
                          np.array([10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8,10 ** 9]), ),
                     ticktext=[f'{format_tick(10 ** 4)}', f'{format_tick(10 ** 5)}', f'{format_tick(10 ** 6)}',
                                 f'{format_tick(10 ** 7)}', f'{format_tick(10 ** 8)}', f'{format_tick(10 ** 9)}'],
                     linewidth=0.5, showline=True, linecolor='black', mirror=True, showgrid=True,
                     gridcolor='lightgrey', gridwidth=0.00001, zerolinewidth=0.00001, range=[symmetric_logarithm(10**4), symmetric_logarithm(10**9)],
                     title_font={"size": 20},
                     tickfont=dict(size=18))

    save_plot_as_pdf(fig, f'{output_data_folder_path}/sample_size_{system_name}.pdf')


def main():
    experiment_FCS_data_path, experiment_AT_data_path, experiment_ALMA_data_path, output_data_folder_path = get_command_line_plots()

    with open(experiment_FCS_data_path, 'r') as f:
        loaded_FCS_data = json.load(f)

    with open(experiment_AT_data_path, 'r') as f:
        loaded_AT_data = json.load(f)

    with open(experiment_ALMA_data_path, 'r') as f:
        loaded_ALMA_data = json.load(f)

    used_delta = [0.1, 0.05, 0.01]
    epsilon_used = [0.1, 0.075, 0.05, 0.025, 0.01, 0.0075, 0.005, 0.0025, 0.001]
    epsilon_used.reverse()

    palette = Cubehelix.make(start=0.3, rotation=-0.5, n=16)
    colors = [f'rgb({c[0]},{c[1]},{c[2]}, 0.01)' for c in palette.colors]

    width_inch = 3.54331
    dpi = 300

    height = 600
    width = math.ceil(width_inch * dpi) * 3 / 4

    systems = ['FCS', 'AT', 'ALMA']

    builded_FCS_data = build_data_for_plot(loaded_FCS_data, epsilon_used, used_delta)
    builded_AT_data = build_data_for_plot(loaded_AT_data, epsilon_used, used_delta)
    builded_ALMA_data = build_data_for_plot(loaded_ALMA_data, epsilon_used, used_delta)

    loaded_data = [builded_FCS_data, builded_AT_data, builded_ALMA_data]

    for i in range(len(systems)):
        make_plot(height, width, epsilon_used, used_delta, loaded_data[i], systems[i],
                  colors, output_data_folder_path)


if __name__ == '__main__':
    main()