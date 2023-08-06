"""Electrophysiology plotting functions"""
import numpy
from decimal import Decimal
import matplotlib.pyplot as plt
from textwrap import wrap

from .style import *


def format_float(f):
    """Format a float to a string without trailing zeros.
    From: https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros"""

    d = Decimal(str(f))
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def define_style(style="explore"):
    """Define the plotting style.

    Args:
        style (str, Style or dict): if str, specifies the name of the style to use (amongst:
            "explore", "paper"). If Style, returns the Style object. If dict, uses the dict to
            instantiate a Style object. Warning: these styles are different from the matplotlib
            styles.
    """

    if isinstance(style, str):
        if style == "explore":
            style = explorer_style
        elif style == "paper":
            style = paper_style
        else:
            raise ValueError("Unknown style: {}".format(style))
    elif isinstance(style, dict):
        style = Style(**style)
    elif not isinstance(style, Style):
        raise ValueError(f"Unknown style of type {type(style)}")

    return style


def get_n_plots(n_voltage_series, n_current_series, shared_axis):
    """Compute the number of plots to plot.

    Args:
        n_voltage_series (int): number of voltage traces.
        n_current_series (int): number of current traces.
        shared_axis (bool): are the voltage and current traces plotted on the same axis?
    """

    if shared_axis or not n_current_series:
        return n_voltage_series
    else:
        return n_voltage_series + n_current_series


def compute_figsize(n_plots, title, style):
    """Compute the figure size for a plot with n_voltage_series voltage traces and,
    optionally, n_current_series current traces.

    Args:
        n_plots (int): number of plots.
    """

    figsize = [6.0, 4.0 * n_plots]

    if style.scale_bars:
        figsize[0] += 1

    if isinstance(title, str):
        figsize[1] += 0.6
    elif isinstance(title, list):
        figsize[1] += 0.3 * len(title)

    if style.show_spines:
        figsize[0] += 1.
        figsize[1] += 1.

    return figsize


def get_text_bbox(text, axis, debug=False):
    """Get the bounding box of a text object in data coordinates"""

    axis.get_figure().canvas.draw()

    transf = axis.transData.inverted()
    bb = text.get_window_extent(renderer=axis.get_figure().canvas.get_renderer())
    bb_data = bb.transformed(transf)

    if debug:
        print("Bounding Box in data coordinates:", bb_data)
        axis.plot([bb_data.x0, bb_data.x1], [bb_data.y0, bb_data.y0], c="c0")
        axis.plot([bb_data.x0, bb_data.x1], [bb_data.y1, bb_data.y1], c="C0")
        axis.plot([bb_data.x0, bb_data.x0], [bb_data.y0, bb_data.y1], c="C0")
        axis.plot([bb_data.x1, bb_data.x1], [bb_data.y0, bb_data.y1], c="C0")

    return bb_data


def compute_scale_bar_length(axis, is_current=False, bar_length=0.15):
    """Compute the length of a scale bar.

    Args:
        axis (matplotlib axis): axis for which to compute the scale bar length.
        is_current (bool): is the scale bar for the current trace?
        bar_length (float): length of the scale bar as a fraction of the axis length.
    """

    valid_time_bar_length = [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    valid_voltage_bar_length = [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100]
    valid_current_bar_length = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50]

    # Find the length of the time bar the closest to the valid lengths
    time_limit = axis.get_xlim()
    target_length = bar_length * (time_limit[1] - time_limit[0])
    time_bar_length = min(valid_time_bar_length, key=lambda x: abs(x - target_length))

    # Find the length of the voltage or current bar the closest to the valid lengths
    IV_limit = axis.get_ylim()
    target_length = bar_length * (IV_limit[1] - IV_limit[0])

    if is_current:
        IV_bar_length = min(valid_current_bar_length, key=lambda x: abs(x - target_length))
    else:
        IV_bar_length = min(valid_voltage_bar_length, key=lambda x: abs(x - target_length))

    return time_bar_length, IV_bar_length


def compute_scale_bar_position(axis, time_bar_length, is_current=False):
    """Compute the position of the scale bar.

    Args:
        axis (matplotlib axis): axis for which to compute the scale bar position.
        time_bar_length (float): length of the time scale bar.
        is_current (bool): is the scale bar for the current trace?
    """

    time_limit = axis.get_xlim()
    IV_limit = axis.get_ylim()

    x_pos = time_limit[0] - 1.2 * time_bar_length
    if is_current:
        y_pos = IV_limit[0] + 0.3 * (IV_limit[1] - IV_limit[0])
    else:
        y_pos = IV_limit[0]

    return x_pos, y_pos


def draw_scale_bars(axis, is_current=False, style="explore"):
    """Draw a ms and nA or mV scale bars on the axis

    Args:
        axis (matplotlib axis): axis on which to draw the scale bars.
        is_current (bool): if True, draw a nA scale bar instead of a mV scale bar.
        time_bar_length (float): length of the time scale bar in percentage of the x-axis length.
        IV_bar_length (float): length of the voltage or current scale bar in percentage of the
            y-axis height.
    """

    style = define_style(style)

    time_bar_length, IV_bar_length = compute_scale_bar_length(axis, is_current)
    scale_bar_origin = compute_scale_bar_position(axis, time_bar_length, is_current)

    # Draw the bars
    color = style.current_color if is_current else style.voltage_color
    scale_bar_settings = dict(color=color, linewidth=style.scale_bars_linewidth, clip_on=False)
    axis.plot(
        [scale_bar_origin[0], scale_bar_origin[0] + time_bar_length],
        [scale_bar_origin[1], scale_bar_origin[1]],
        **scale_bar_settings,
    )
    axis.plot(
        [scale_bar_origin[0], scale_bar_origin[0]],
        [scale_bar_origin[1], scale_bar_origin[1] + IV_bar_length],
        **scale_bar_settings,
    )

    # Add the labels at the origin of the bars
    time_label = axis.text(
        scale_bar_origin[0],
        scale_bar_origin[1],
        f'{format_float(time_bar_length)} ms',
        horizontalalignment="center",
        verticalalignment="bottom",
        fontsize=style.scale_bars_fontsize,
    )

    if is_current:
        iv_label = axis.text(
            scale_bar_origin[0],
            scale_bar_origin[1],
            f'{format_float(IV_bar_length)} nA',
            horizontalalignment="left",
            verticalalignment="center",
            fontsize=style.scale_bars_fontsize,
        )
    else:
        iv_label = axis.text(
            scale_bar_origin[0],
            scale_bar_origin[1],
            f'{format_float(IV_bar_length)} mV',
            horizontalalignment="left",
            verticalalignment="center",
            fontsize=style.scale_bars_fontsize,
        )

    # Move the labels such that they do not overlap with the scale bars
    text_height = get_text_bbox(time_label, axis).height
    time_label.set_position(
        (scale_bar_origin[0] + 0.5 * time_bar_length, scale_bar_origin[1] - 1.8 * text_height)
    )

    text_length = get_text_bbox(iv_label, axis).width
    iv_label.set_position(
        (scale_bar_origin[0] - 1.3 * text_length, scale_bar_origin[1] + 0.5 * IV_bar_length)
    )


def hide_spines(axis):
    """Hide the spines of an axis.

    Args:
        axis (matplotlib axis): axis for which to hide the spines.
    """

    for spine in axis.spines.values():
        spine.set_visible(False)

    axis.set_xticks([])
    axis.set_yticks([])


def draw_title(title, axis, style):
    """Add a title to an axis. Wrap it at 50 characters if wrapping is enable in the style.
    Note: Does not use suptitle because it does not work well with tight layout."""

    if style.wrap_title:
        title_format = "\n".join(wrap(title, 50))
    else:
        title_format = title

    axis.set_title(title_format, fontsize=style.title_fontsize)


def define_axis(axis, style, title, voltage_series, current_series):
    """Creates or check the validity of the axis on which the data will be plotted."""

    tmp_v = numpy.asarray(voltage_series)
    tmp_i = numpy.asarray(current_series) if current_series is not None else None

    n_voltage_series = 1 if tmp_v.ndim == 1 else tmp_v.shape[0]

    if current_series is None:
        n_current_series = 0
    else:
        n_current_series = 1 if tmp_i.ndim == 1 else tmp_i.shape[0]

    n_plots = get_n_plots(n_voltage_series, n_current_series, shared_axis=style.shared_axis)

    if axis is None:
        figsize = compute_figsize(n_plots=n_plots, title=title, style=style)
        fig, axis = plt.subplots(n_plots, 1, figsize=figsize)
    else:
        if isinstance(axis, (list, numpy.ndarray)):
            if len(axis) != n_plots:
                raise ValueError(
                    "The number of axis provided is not the same as the number of series to plot."
                )
            fig = axis[0].get_figure()
        else:
            if n_plots > 1 and not style.shared_axis:
                raise ValueError(
                    "The total number of traces is greater than 1, but only one axis was provided."
                )
            fig = axis.get_figure()

    return fig, axis


def plot_trace(
    time_series,
    voltage_series,
    current_series=None,
    title=None,
    axis=None,
    style="explore",
):
    """Plot a single electrophysiological trace (voltage and, optionally, current).

    Args:
        time_series (list or numpy.array): time series in ms.
        voltage_series (list or numpy.array): voltage series in mV.
        current_series (list or numpy.array): current series in nA.
        title (str): title of the plot.
        axis (axis or list of axis): matplotlib axis on which to plot.
        style (str, Style or dict): if str, specifies the name of the style to use (amongst:
            "explore", "paper"). If dict, uses the dict to instantiate a Style object. Warning:
            these styles are different from the matplotlib styles.
    """

    style = define_style(style)

    fig, axis = define_axis(axis, style, title, voltage_series, current_series)

    if current_series is not None:
        axis_current = axis if style.shared_axis else axis[0]
        axis_voltage = axis.twinx() if style.shared_axis else axis[-1]
    else:
        axis_voltage = axis
        axis_current = None

    if current_series is not None:
        axis_current.plot(
            time_series,
            current_series,
            color=style.current_color,
            alpha=style.current_alpha,
            linewidth=style.linewidth
        )
    axis_voltage.plot(
        time_series,
        voltage_series,
        color=style.voltage_color,
        alpha=style.voltage_alpha,
        linewidth=style.linewidth
    )

    # Set the limits of the axis to the limits of the data
    axis_voltage.set_xlim(time_series[0], time_series[-1])
    axis_voltage.set_ylim(voltage_series.min(), voltage_series.max())
    if current_series is not None:
        axis_current.set_xlim(time_series[0], time_series[-1])
        axis_current.set_ylim(current_series.min(), current_series.max())

    if not style.show_spines:
        hide_spines(axis_voltage)
        if axis_current:
            hide_spines(axis_current)

    if style.scale_bars:
        draw_scale_bars(axis_voltage, is_current=False, style=style)
        if axis_current:
            draw_scale_bars(axis_current, is_current=True, style=style)
    else:
        axis_voltage.set_xlabel("Time (ms)", fontsize=style.label_fontsize)
        axis_voltage.set_ylabel("Voltage (mV)", fontsize=style.label_fontsize)
        if axis_current:
            axis_current.set_xlabel("Time (ms)", fontsize=style.label_fontsize)
            axis_current.set_ylabel("Current (nA)", fontsize=style.label_fontsize)

    if title is not None:
        tmp_axis = axis_voltage if axis_current is None else axis_current
        draw_title(title, axis=tmp_axis, style=style)

    fig.tight_layout()

    return fig, axis


def plot_traces(
    time_series,
    voltage_series,
    current_series=None,
    title=None,
    axis=None,
    style="explore",
):
    """Plot multiple electrophysiological traces (voltage and, optionally, current).

    Args:
        time_series (list of list or numpy.array): multiple time series in ms.
        voltage_series (list of list or numpy.array): multiple voltage series in mV.
        current_series (list of list or numpy.array): multiple current series in nA.
        title (str or list of string): title of the plot or plots. If str, the title is only
            display on the top axis.
        axis (axis or list of axis): matplotlib axis on which to plot. If None, a new figure is
            created. If current is to be plotted and shared_axis is False, the axis must be a
            list and the current will be plotted on the first axis of the list.
        style (str, Style or dict): if str, specifies the name of the style to use (amongst:
            "explore", "paper"). If dict, uses the dict to instantiate a Style object. Warning:
            these styles are different from the matplotlib styles.
    """

    if len(time_series) != len(voltage_series):
        raise ValueError("The number of time series and voltage series must be the same.")

    if current_series is not None:
        if len(time_series) != len(current_series):
            raise ValueError("The number of time series and current series must be the same.")

    style = define_style(style)

    fig, axis = define_axis(axis, style, title, voltage_series, current_series)

    if title is None:
        titles = [None] * len(time_series)
    elif isinstance(title, str):
        titles = [title] + [None] * (len(time_series) - 1)
    elif isinstance(title, list):
        if len(title) != len(time_series):
            raise ValueError("The number of titles and time series must be the same.")
        titles = title

    for i in range(len(time_series)):

        tmp_current_series = current_series[i] if current_series is not None else None

        if tmp_current_series is not None:
            tmp_axis = axis[i] if style.shared_axis else axis[i*2:i*2+2]
        else:
            tmp_axis = axis[i]

        _, _ = plot_trace(
            time_series[i],
            voltage_series[i],
            current_series=tmp_current_series,
            title=titles[i],
            axis=tmp_axis,
            style=style,
        )

    fig.tight_layout()

    return fig, axis
