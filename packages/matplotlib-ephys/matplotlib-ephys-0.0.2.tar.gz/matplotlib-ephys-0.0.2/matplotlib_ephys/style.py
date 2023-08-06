"""Style classes definition"""
from dataclasses import dataclass


@dataclass
class Style:
    """Abstract class listing the existing settings

    Args:
        shared_axis (bool): if True, the voltage and current traces are plotted on the same axis.
        show_spines (bool): if True, shows the spine (frame) around the plots.
        scale_bars (bool): if True, draws mV, nA and ms scale bars on the plots.
        linewidth (float): width of the voltage and current traces.
        voltage_color (str): color of the voltage traces.
        voltage_alpha (float): transparency of the voltage traces.
        current_color (str): color of the current traces.
        current_alpha (float): transparency of the current traces.
        wrap_title (bool): should the title be wrapped at 50 characters if too long. Put False if
            you formatted the title yourself.
        title_fontsize (float): fontsize of the title.
        scale_bars_fontsize (float): fontsize of the scale bar labels.
        scale_bars_linewidth (float): width of the scale bars.
        label_fontsize (float): fontsize of the labels.
    """

    shared_axis: bool = False
    show_spines: bool = True

    scale_bars: bool = False
    scale_bars_fontsize: int = 10.
    scale_bars_linewidth: float = 1.

    linewidth: int = 1.
    voltage_color: str = "black"
    voltage_alpha: float = 1.
    current_color: str = "gray"
    current_alpha: float = 1.

    wrap_title: bool = True
    title_fontsize: int = 14.
    label_fontsize: int = 12.


# Style useful for data exploration, with splines
explorer_style = Style(
    shared_axis=False,
    show_spines=True,
    scale_bars=False,
    linewidth=1.,
    voltage_color="black",
    voltage_alpha=1.,
    current_color="gray",
    current_alpha=1.,
    wrap_title=True,
    title_fontsize=14.,
    scale_bars_fontsize=10.,
    scale_bars_linewidth=1.,
    label_fontsize=12.,
)

# For publications, class to display voltage traces without splines and with scale bars
paper_style = Style(
    shared_axis=True,
    show_spines=False,
    scale_bars=True,
    linewidth=1.,
    voltage_color="black",
    voltage_alpha=0.9,
    current_color="red",
    current_alpha=0.9,
    wrap_title=True,
    title_fontsize=14.,
    scale_bars_fontsize=10.,
    scale_bars_linewidth=1.,
    label_fontsize=12.,
)
