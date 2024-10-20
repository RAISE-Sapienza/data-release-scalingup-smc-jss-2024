import plotly.io as io_handler
import plotly.graph_objects as go

import numpy as np
import math
import contextlib

from typing import List


def symmetric_logarithm(x,base=10,C=1,shift=1):
    return np.sign(x)*(np.log10(1+abs(x)/(10^C)))


def format_tick(n: float):
    frac, whole = math.modf(n*1000)
    if frac == 0.0:
        m, e = f"{n:.0e}".split("e")
    else:
        m, e = f"{n:.1e}".split("e")
    e = int(e)
    return f"10<sup>{e}</sup>"

def format_legend(n: float):
    frac, whole = math.modf(n*1000)
    if frac == 0.0:
        m, e = f"{n:.0e}".split("e")
    else:
        m, e = f"{n:.1e}".split("e")
    e = int(e)
    return f"{m}e-0{abs(e)}"


def save_plot_as_pdf(plot_fig: go.Figure, name_path: str) -> None:
    io_handler.full_figure_for_development(plot_fig, warn=False)
    io_handler.write_image(plot_fig, name_path, format='pdf', engine="orca")


def get_used_epsilon() -> List[float]:
    epsilon_used = [0.1, 0.075, 0.05, 0.025, 0.01, 0.0075, 0.005, 0.0025, 0.001]
    epsilon_used.reverse()
    return epsilon_used

def get_used_delta() -> List[float]:
    used_delta = [0.1, 0.05, 0.01]
    return used_delta