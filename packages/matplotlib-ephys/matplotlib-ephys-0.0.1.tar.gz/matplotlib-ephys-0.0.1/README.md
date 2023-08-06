# matplotlib-ephys

Introduction
============

Matplotlib-ephys is a Python package that does only one thing. 
It can be used to plot electrophysiological recordings, in the form of voltage and current time series.
It has however, the interesting capability of being to plot bars, which can be tedious to do manually.

Requirements
============

* `Python 3.6+ <https://www.python.org/downloads/release/python-360/>`
* `Pip <https://pip.pypa.io>` (installed by default in newer versions of Python)
* `Numpy <http://www.numpy.org>` (automatically installed by pip)
* `Matplotlib <https://matplotlib.org/>` (automatically installed by pip)
* The instruction below are written assuming you have access to a command shell on Linux / UNIX / MacOSX / Cygwin

Installation
============

To install the package, run the following command in your terminal:
```
pip install matplotlib-ephys
```

Quick Start
===========

The present package provides a set of functions for plotting electrophysiological recordings.
It is only able to plot voltage and current time series provided as lists or numpy arrays.

The package has two main functionss: `plot_trace` and `plot_traces`.
The former except a single trace as input, while the latter accepts a list of traces.

Here is an example using the data present in the test folder:
```
import numpy
import matplotlib.pyplot as plt
import matplotlib_ephys as mpe

data = numpy.asarray([numpy.load(f"./tests/test_data_{i}.npy") for i in range(5)])

fig, axis = mpe.plot_traces(
    time_series=data[:, 0],
    voltage_series=data[:, 2],
    current_series=data[:, 1],
    title="Example of plotting multiple traces",
    style="explore",
)

plt.show()
plt.close(fig)
```

Note that providing current series is not mandatory.


Plotting with style
===========

Unlike when using Matplotlib directly, the settings and options related to the style of the plots are not directly accessible.
Instead, the package provides a set of predifined styles, which can be specified when by calling the functions `plot_trace` and `plot_traces`.
As of now, two styles are available: `explore` and `paper`.

It is also possible to provide a custom style, either by providing a custom instance of the class Style (see style.py), or by providing a dictionary of settings.
The existing settings and their default values are:
* shared_axis (bool, default: False): if True, the voltage and current traces are plotted on the same axis.
* show_spines (bool, default: True): if True, shows the spine (frame) around the plots.
* scale_bars (bool, default: False): if True, draws mV, nA and ms scale bars on the plots.
* linewidth (float, default: 1): width of the voltage and current traces.
* voltage_color (str, default: "black"): color of the voltage traces.
* voltage_alpha (float, default: 1): transparency of the voltage traces.
* current_color (str, default: "gray"): color of the current traces.
* current_alpha (float, default: 1): transparency of the current traces.
* wrap_title (bool, default: True): should the title be wrapped at 50 characters if too long. Put False if you formatted the title yourself.
* title_fontsize (float, default: 14): fontsize of the title.
* scale_bars_fontsize (float, default: 10): fontsize of the scale bar labels.
* scale_bars_linewidth (float, default: 1): width of the scale bars.
* label_fontsize (float, default: 12): fontsize of the labels.

Drawing scale bars
===========

Scale bars will be drawn on the plots if the style setting `scale_bars` is set to True.

The `draw_scale_bars` function can also be used as a stand alone function if you have your own figures. To do so, provide the axis object as follows:
```
draw_scale_bars(axis=your_axis, is_current=False, style="paper")
```
The `is_current` parameter indicate if the data on the axis is current or voltage.
This function except the x-axis to be time in ms and the y-axis to be the matching voltage or current times series in mV and nA respectively.
