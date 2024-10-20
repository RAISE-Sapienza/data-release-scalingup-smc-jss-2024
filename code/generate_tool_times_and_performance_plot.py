from lib.cmd_lib import get_command_line_plots
from lib.utils_lib import save_plot_as_pdf, get_used_delta, get_used_epsilon
import plotly.graph_objects as go

from typing import List
import numpy as np
import json, math

from palettable.cubehelix import Cubehelix

from plotly.subplots import make_subplots


def build_data_for_plot(loaded_data: dict, used_epsilon: List[float], used_delta: List[float], workers: List[int]):
    builded_data = dict()

    for w in workers:
        loaded_data_worker = loaded_data[f'workers{w}']
        builded_data[f'workers{w}'] = dict()

        for delta in used_delta:
            builded_data[f'workers{w}'][f'delta_{delta}'] = dict()
            for epsilon in used_epsilon:
                mean_exec_times = loaded_data_worker[f'delta{delta}_epsilon{epsilon}']['time']['mean']
                error_exec_times = loaded_data_worker[f'delta{delta}_epsilon{epsilon}']['time']['error']
                list_exec_times = loaded_data_worker[f'delta{delta}_epsilon{epsilon}']['time']['values_list']
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}'] = dict()
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times'] = dict()
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['mean'] = mean_exec_times
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['error'] = error_exec_times
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list'] = list_exec_times

                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency'] = dict()
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['values_list'] = []
                for i in range(len(builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list'])):
                    time_1worker = builded_data[f'workers{1}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list'][i]
                    time_parallel_worker = builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list'][i]
                    efficiency = (time_1worker / time_parallel_worker) / w * 100
                    builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['values_list'].append(efficiency)

                data = builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['values_list']
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['mean'] = np.mean(data)
                builded_data[f'workers{w}'][f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['error'] = np.std(data, ddof=0) / np.sqrt(np.size(data))

    return builded_data


def tickvals_ticktext_from_casestudy(case_study_name: str):
    if case_study_name == 'FCS' or case_study_name == 'AT':
        tickvals = [1, 60, 3600, 86400, 86400*30]
        ticktext = ['1 s', '1 m', '1 h', '1 d', '1 mo']
        axis_range = (0, np.log10(86400*24)+1)
    else:
        tickvals = [1, 60, 3600, 86400, 86400*30, 86400*30*12, 86400*30*12*20]
        ticktext = ['1 s', '1 m', '1 h', '1 d', '1 mo', '1 y', '20 y']
        axis_range = (0, np.log10(tickvals[-1]) + 1)

    return list(tickvals), ticktext, axis_range


def get_minorticks_tickvals_ticktext_from_casestudy(case_study_name: str):
    minor_tick_vals = [15, 30, 45, #minor ticks for seconds
                       60*15, 60*30, 60*45, #minor ticks for minutes
                       60*60*6, 60*60*12, 60*60*18, # minor ticks for hours
                       60*60*24*7, 60*60*24*14, 60*60*24*21, # minor ticks for days
                       60*60*24*30*3, 60*60*24*30*6, 60*60*24*30*9, # minor ticks for months
                       60*60*24*30*12*5, 60*60*24*30*12*10, 60*60*24*30*12*15
                      ]

    '''
    minor_tick_text = ["15s", "", "",
                       "15m", "", "",
                       "6h",  "", "",
                       "7 days", "", "",
                       "3 months", "", "",
                       "5 years", "", ""]
    '''
    minor_tick_text = ["", "", "",
                       "", "", "",
                       "", "", "",
                       "", "", "",
                       "", "", "",
                       "", "", ""]
    return minor_tick_vals, minor_tick_text


def add_ticks_annotation(fig, case_study_name):
    if case_study_name == 'ALMA':
        fig.add_annotation(text="15 s",
                       xref="paper", yref="paper",
                       x=-0.055, y=0.100,
                       showarrow=False,
                       font_size=17,
                       borderwidth=0,
                       bordercolor="grey",
                       bgcolor="rgba(255,255,255, 0)",
                       visible=True,
                       textangle=0
                       )

        fig.add_annotation(text="15 m",
                           xref="paper", yref="paper",
                           x=-0.065, y=0.285,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="6 h",
                           xref="paper", yref="paper",
                           x=-0.045, y=0.445,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="7 d",
                           xref="paper", yref="paper",
                           x=-0.045, y=0.59,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="3 mo",
                           xref="paper", yref="paper",
                           x=-0.065, y=0.73,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="5 y",
                           xref="paper", yref="paper",
                           x=-0.043, y=0.86,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )
    else:
        fig.add_annotation(text="15 s",
                           xref="paper", yref="paper",
                           x=-0.055, y=0.145,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="15 m",
                           xref="paper", yref="paper",
                           x=-0.065, y=0.4005,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="6 h",
                           xref="paper", yref="paper",
                           x=-0.0455, y=0.595,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )

        fig.add_annotation(text="7 d",
                           xref="paper", yref="paper",
                           x=-0.045, y=0.815,
                           showarrow=False,
                           font_size=17,
                           borderwidth=0,
                           bordercolor="grey",
                           bgcolor="rgba(255,255,255, 0)",
                           visible=True,
                           textangle=0
                           )


def make_plot(height: int, width: int, loaded_experiments: dict, used_epsilon: List[float], used_delta: List[float], colors,
              case_study_name: str, n_workers: int, output_plot_path:str):

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    x_data = [str(epsilon*100) for epsilon in used_epsilon]

    fig.add_trace(go.Scatter(x=x_data, y=[100 for _ in range(len(used_epsilon))],
                             mode='lines', line=dict(color='grey', width=2, dash='dash'), showlegend=False),
                             secondary_y=True,
                             )

    shapes = ['circle-open', 'square-open', 'diamond-open']
    j = 5
    shape_idx = 0
    rank_idx=1
    delta_notation=['10<sup>-1</sup>', '5x10<sup>-2</sup>', '10<sup>-2</sup>']
    delta_notation_idx = 0
    for delta in used_delta:
        max_time = [max(loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list']) - loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['times']['mean'] for epsilon in used_epsilon]
        min_time = [loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['times']['mean'] - min(loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['times']['values_list']) for epsilon in used_epsilon]
        mean_time = [loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['times']['mean'] for epsilon in used_epsilon]

        fig.add_trace(go.Scatter(x=x_data, y=mean_time,
                                 name=f'time with \u03b4={delta_notation[delta_notation_idx]}',
                                 legendrank=rank_idx,
                                 showlegend=True,
                                 mode='lines+markers',
                                 marker=dict(
                                     size=15,
                                     symbol=shapes[shape_idx],
                                     color=colors[j]),
                                 line=dict(color=colors[j], width=1, dash='solid'),
                                 error_y=dict(
                                     type='data',
                                     symmetric=False,
                                     array=max_time,
                                     arrayminus=min_time)
                                 ))
        rank_idx += 1
        max_efficiency = [max(loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['values_list']) -
                          loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['mean'] for epsilon
                          in used_epsilon]
        min_efficiency = [loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['mean'] - min(
            loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['values_list']) for epsilon
                          in used_epsilon]
        mean_efficiency = [loaded_experiments[f'delta_{delta}'][f'epsilon_{epsilon}']['efficiency']['mean'] for epsilon
                           in
                           used_epsilon]

        fig.add_trace(go.Scatter(x=x_data, y=mean_efficiency,
                                 showlegend=True,
                                 mode='lines+markers',
                                 name=f'efficiency with \u03b4={delta_notation[delta_notation_idx]}',
                                 marker=dict(
                                     size=15,
                                     symbol=shapes[shape_idx],
                                     color=colors[j]),
                                 line=dict(color=colors[j], width=2, dash='dash'),
                                 error_y=dict(
                                     type='data',
                                     symmetric=False,
                                     array=max_efficiency,
                                     arrayminus=min_efficiency)
                                 ), secondary_y=True)
        delta_notation_idx += 1
        j += 3
        shape_idx += 1

    if n_workers <= 256 or case_study_name == 'ALMA':
        x_legend = 0.01
        y_legend = 0.02
    else:
        x_legend = 0.01
        y_legend = 0.6

    fig.update_layout(showlegend=True, height=height, width=width, title={
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, plot_bgcolor='rgba(0,0,0,0)', margin=dict(r=0, t=0, l=0, b=0),  # bargap=0.5,
                      legend=dict(font=dict(size=20), itemwidth=30, borderwidth=1.35,
                                  yanchor="bottom", y=y_legend, xanchor="left", x=x_legend,
                                  bgcolor='rgba(255,255,255, 1.0)'),
                      )

    add_ticks_annotation(fig, case_study_name)


    fig.update_xaxes( linewidth=1.5, linecolor='black', showline=True, showgrid=True, gridwidth=0.00001,
                     gridcolor='lightgrey', title_font={"size": 26}, tickfont=dict(size=23), mirror='ticks',
                     ticks="inside",
                     tickwidth=0, ticklen=0, title_standoff=0)

    tickvals, ticktext, axis_range = tickvals_ticktext_from_casestudy(case_study_name)
    minor_tickvals, minor_ticktext = get_minorticks_tickvals_ticktext_from_casestudy(case_study_name)

    fig.update_yaxes(linewidth=1.5, linecolor='black', showline=True, showgrid=True, gridwidth=0.00001,
                     gridcolor='lightgrey', zeroline=True, zerolinecolor='lightgrey', zerolinewidth=0.00001,
                     showticklabels=True, type="log",
                     title_font={"size": 26}, tickfont=dict(size=23), mirror='ticks', ticks="inside", tickwidth=0,
                     title_standoff=0, secondary_y=False,
                     tickvals=list(tickvals)+list(minor_tickvals), ticktext=ticktext+minor_ticktext,
                     range=[axis_range[0], axis_range[1]])

    fig.update_yaxes(secondary_y=True, range=[0, 103], tickvals=[i for i in range(0, 101, 10)],
                     ticklen=0, ticktext=["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
                     title_font={"size": 26}, tickfont=dict(size=23),
                     tickformat="%", title_standoff=0
                     )

    save_plot_as_pdf(fig, f'{output_plot_path}/{case_study_name}/parallel_performance_{case_study_name}_{n_workers}workers.pdf')




def main():
    experiment_FCS_data_path, experiment_AT_data_path, experiment_ALMA_data_path, output_data_path = get_command_line_plots()

    with open(experiment_FCS_data_path, 'r') as f:
        loaded_FCS_data = json.load(f)

    with open(experiment_AT_data_path, 'r') as f:
        loaded_AT_data = json.load(f)

    with open(experiment_ALMA_data_path, 'r') as f:
        loaded_ALMA_data = json.load(f)

    width_inch = 3.54331
    dpi = 300

    height = 600
    width = math.ceil(width_inch * dpi) * 3/4

    case_study_data = [loaded_FCS_data, loaded_AT_data, loaded_ALMA_data]
    case_study_name = ['FCS', 'AT', 'ALMA']

    used_delta = get_used_delta()
    epsilon_used = get_used_epsilon()
    used_workers = [1, 128, 512, 1024, 2048]

    palette = Cubehelix.make(start=0.3, rotation=-0.5, n=16)
    colors = [f'rgb({c[0]},{c[1]},{c[2]})' for c in palette.colors]

    for i, case_study_data in enumerate(case_study_data):
        builded_case_study_data = build_data_for_plot(case_study_data, epsilon_used, used_delta, used_workers)
        for w in used_workers:
            builded_case_study_data_with_worker = builded_case_study_data[f'workers{w}']
            make_plot(height, width, builded_case_study_data_with_worker, epsilon_used, used_delta, colors,
                      case_study_name[i], w, output_data_path)


if __name__ == '__main__':
    main()