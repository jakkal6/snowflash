import numpy as np
import matplotlib.pyplot as plt

"""
Generalised plotting wrappers
"""


def setup_fig_ax(ax, figsize):
    """Setup fig, ax, checking if ax already provided

    parameters
    ----------
    ax : Axes
    figsize : [width, height]
    """
    fig = None

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    return fig, ax


def setup_subplots(n_sub,
                   max_cols=1,
                   sub_figsize=(6, 5),
                   **kwargs):
    """Constructs fig for given number of subplots

    returns : fig, ax

    parameters
    ----------
    n_sub : int
        number of subplots (axes)
    max_cols : int
        maximum number of columns to arange subplots
    sub_figsize : tuple
        figsize of each subplot
    **kwargs :
        args to be parsed to plt.subplots()
    """
    n_rows = int(np.ceil(n_sub / max_cols))
    n_cols = {False: 1, True: max_cols}.get(n_sub > 1)
    figsize = (n_cols * sub_figsize[0], n_rows * sub_figsize[1])

    return plt.subplots(n_rows, n_cols, figsize=figsize, **kwargs)


def check_ax(ax, figsize):
    """Setup fig, ax if ax is not provided

    parameters
    ----------
    ax : pyplot Axis
    figsize : [width, height]
    """
    fig = None

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    return fig, ax


def set_ax_all(ax,
               x_var=None, y_var=None,
               x_scale=None, y_scale=None,
               x_label=None, y_label=None,
               x_lims=None, y_lims=None,
               legend=False,
               legend_loc=None,
               title=False,
               title_str=None):
    """Set all ax properties

    parameters
    ----------
    ax : pyplot Axis
    x_var : str
    y_var : str
    x_scale : str
    y_scale : str
    x_label : str
    y_label : str
    x_lims : [min, max]
    y_lims : [min, max]
    legend : bool
    legend_loc : str
    title : bool
    title_str : str
    """
    set_ax_scales(ax, x_scale=x_scale, y_scale=y_scale)
    set_ax_labels(ax, y_label=y_label, x_label=x_label)
    set_ax_lims(ax, x_lims=x_lims, y_lims=y_lims)
    set_ax_legend(ax, legend=legend, loc=legend_loc)
    set_ax_title(ax, string=title_str, title=title)


def set_ax_scales(ax, x_scale=None, y_scale=None):
    """Set axis scales (linear, log)

    parameters
    ----------
    ax : pyplot Axis
    x_scale : str
    y_scale : str
    """
    x_scale = {None: 'linear'}.get(x_scale, x_scale)
    y_scale = {None: 'linear'}.get(y_scale, y_scale)

    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)


def set_ax_title(ax, string, title):
    """Set axis title

    parameters
    ----------
    ax : pyplot Axis
    string : str
    title : bool
    """
    if title:
        ax.set_title(string)


def set_ax_lims(ax, x_lims=None, y_lims=None):
    """Set x and y axis limits

    parameters
    ----------
    ax : pyplot Axis
    x_lims : [min, max]
    y_lims : [min, max]
    """
    ax.set_xlim(x_lims)
    ax.set_ylim(y_lims)


def set_ax_labels(ax, x_label=None, y_label=None):
    """Set x and y axis limits

    parameters
    ----------
    ax : pyplot Axis
    x_label : str
    y_label : str
    """
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)


def set_ax_legend(ax, legend, loc=None):
    """Set axis legend

    parameters
    ----------
    ax : pyplot Axis
    legend : bool
    loc : str or int
    """
    if legend:
        ax.legend(loc=loc)
