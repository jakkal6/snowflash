import matplotlib.pyplot as plt

# snowglobes
from . import plot_tools
from . import config
from .snow_tools import y_column


def plot_integrated(integrated, y_var, prog_table,
                    channel='total',
                    x_var='m_fe',
                    x_scale=None,
                    y_scale=None,
                    x_lims=None,
                    y_lims=None,
                    marker='.',
                    ax=None,
                    legend=True,
                    legend_loc=None,
                    figsize=None,
                    label=None,
                    color=None,
                    data_only=False,
                    ):
    """Plot quantity from integrated table

    parameters
    ----------
    integrated : xr.Dataset}
        table of time-integrated quantities
    y_var : 'counts' or 'energy'
    prog_table : pd.DataFrame
    x_var : str
    channel : str
    x_scale : str
    y_scale : str
    x_lims : [low, high]
    y_lims : [low, high]
    marker : str
    ax : Axis
    legend : bool
    legend_loc : int or str
    figsize : (width, height)
    label : str
    color : str
    data_only : bool
    """
    fig, ax = setup_fig_ax(ax=ax, figsize=figsize)
    y_col = y_column(y_var=y_var, channel=channel)

    ax.plot(prog_table[x_var], integrated[y_col],
            marker=marker,
            ls='none',
            label=label,
            color=color)

    if not data_only:
        plot_tools.set_ax_all(ax=ax,
                              x_var=x_var,
                              y_var=y_var,
                              x_scale=x_scale,
                              y_scale=y_scale,
                              x_lims=x_lims,
                              y_lims=y_lims,
                              legend=legend,
                              legend_loc=legend_loc)

    return fig


def plot_channels(integrated, y_var, prog_table, channels,
                  x_var='m_fe',
                  x_scale=None, y_scale=None,
                  x_lims=None, y_lims=None,
                  marker='.',
                  legend=False,
                  legend_loc=None,
                  figsize=None,
                  axes=None,
                  color=None,
                  label=None,
                  data_only=False,
                  ):
    """Plot time-integrated variable for all channels

    parameters
    ----------
    integrated : xr.Dataset
    y_var : 'counts' or 'energy'
    prog_table : pd.DataFrame
    channels : [str]
    x_var : str
    x_scale : str
    y_scale : str
    x_lims : [low, high]
    y_lims : [low, high]
    marker : str
    legend : bool
    legend_loc : int or str
    figsize : (width, height)
    axes : [Axis]
        len(axes) must equal len(channels)
    color : str
    label : str
    data_only : bool
    """
    fig = None
    if axes is None:
        fig, axes = plt.subplots(len(channels), figsize=figsize, sharex=True)

    for i, channel in enumerate(channels):
        plot_integrated(integrated=integrated,
                        y_var=y_var,
                        channel=channel,
                        x_var=x_var,
                        prog_table=prog_table,
                        marker=marker,
                        color=color,
                        label=label,
                        ax=axes[i],
                        data_only=True)

        if not data_only:
            plot_tools.set_ax_all(ax=axes[i],
                                  x_var=x_var,
                                  y_var=y_var,
                                  x_scale=x_scale,
                                  y_scale=y_scale,
                                  x_lims=x_lims,
                                  y_lims=y_lims,
                                  y_label=f'{y_var} ({channel})')
    if legend:
        axes[0].legend(loc=legend_loc)

    plt.subplots_adjust(hspace=0)
    return fig


def plot_difference(tables, y_var, prog_table, ref_model_set,
                    channel='total',
                    x_var='m_fe',
                    x_scale=None,
                    y_scale=None,
                    x_lims=None,
                    y_lims=None,
                    marker='.',
                    ax=None,
                    legend=True,
                    figsize=None):
    """Plot differences relative to given model_set

    parameters
    ----------
    tables : {model_set: xr.Dataset}
        collection of integrated_tables to plot
    y_var : str
    channel : str
    prog_table : pd.DataFrame
    ref_model_set : str
        which model_set to use as the baseline for comparison
    x_var : str
    x_scale : str
    y_scale : str
    x_lims : [low, high]
    y_lims : [low, high]
    marker : str
    ax : Axis
    legend : bool
    figsize : (width, height)
    """
    fig, ax = setup_fig_ax(ax=ax, figsize=figsize)
    ref_table = tables[ref_model_set]
    x = prog_table[x_var]
    y_col = y_column(y_var=y_var, channel=channel)

    for model_set, table in tables.items():
        if model_set == ref_model_set:
            continue

        ax.plot(x, table[y_col] - ref_table[y_col],
                marker=marker,
                ls='none',
                label=model_set,
                color=config.colors.get(model_set))

    ax.hlines(0, x.min(), x.max(),
              linestyles='--',
              colors=config.colors.get(ref_model_set))

    plot_tools.set_ax_all(ax=ax,
                          x_var=x_var,
                          y_var=y_var,
                          x_scale=x_scale,
                          y_scale=y_scale,
                          x_lims=x_lims,
                          y_lims=y_lims,
                          legend=legend)

    return fig


def plot_timebin(timebin_table, y_var, mass,
                 channel='total',
                 x_scale=None,
                 y_scale=None,
                 ax=None,
                 legend=False,
                 figsize=None,
                 label=None,
                 color=None,
                 data_only=False,
                 ):
    """Plot timebinned variable from table

    parameters
    ----------
    timebin_table : pd.DataFrame
    y_var : 'counts' or 'energy'
    mass : float or int
    channel : str
    y_scale : str
    x_scale : str
    ax : Axis
    legend : bool
    figsize : (width, height)
    label : str
    color : str
    data_only : bool
    """
    fig, ax = setup_fig_ax(ax=ax, figsize=figsize)
    y_col = y_column(y_var=y_var, channel=channel)

    table = timebin_table.sel(mass=mass)
    ax.step(table['time'], table[y_col],
            where='post',
            label=label,
            color=color)

    if not data_only:
        plot_tools.set_ax_all(ax=ax,
                              x_var='time',
                              y_var=y_var,
                              x_scale=x_scale,
                              y_scale=y_scale,
                              legend=legend)
    return fig


def plot_cumulative(cumulative, y_var, mass,
                    channel='total',
                    x_scale=None,
                    y_scale=None,
                    ax=None,
                    label=None,
                    color=None,
                    legend=True,
                    linestyle=None,
                    figsize=None,
                    data_only=False,
                    ):
    """Plot cumulative quantity

    parameters
    ----------
    cumulative : xr.Dataset
        table of cumulative quantities
    y_var : 'counts' or 'energy'
    mass : float or int
    channel : str
    y_scale : str
    x_scale : str
    ax : Axis
    label : str
    color : str
    legend : bool
    linestyle : str
    figsize : (width, height)
    data_only : bool
    """
    fig, ax = setup_fig_ax(ax=ax, figsize=figsize)
    y_col = y_column(y_var=y_var, channel=channel)

    table = cumulative.sel(mass=mass)
    ax.step(table['n_bins'], table[y_col],
            where='pre',
            label=label,
            color=color,
            linestyle=linestyle)

    if not data_only:
        plot_tools.set_ax_all(ax=ax,
                              x_var='timebins [5 ms]',
                              y_var=y_var,
                              x_scale=x_scale,
                              y_scale=y_scale,
                              legend=legend)

    return fig


# ===============================================================
#                      Misc.
# ===============================================================
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
