import matplotlib.pyplot as plt

# snowglobes
from . import plot_tools
from . import config


def plot_summary(tables, column, prog_table,
                 x_var='m_fe',
                 x_scale=None, y_scale=None,
                 x_lims=None, y_lims=None,
                 marker='.',
                 ax=None,
                 legend=True,
                 figsize=None):
    """Plot quantity from summary table

    parameters
    ----------
    tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
    prog_table : pd.DataFrame
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

    for model_set, table in tables.items():
        ax.plot(prog_table[x_var], table[column],
                marker=marker, ls='none', label=model_set,
                color=config.colors.get(model_set))

    plot_tools.set_ax_all(ax=ax, x_var=x_var, y_var=column[:3],
                          x_scale=x_scale, y_scale=y_scale,
                          x_lims=x_lims, y_lims=y_lims,
                          legend=legend)

    plt.tight_layout()
    return fig, ax


def plot_all_channels(tables, var, prog_table, channels,
                      x_var='m_fe',
                      x_scale=None, y_scale=None,
                      x_lims=None, y_lims=None,
                      marker='.',
                      ax=None,
                      legend=True,
                      figsize=None):
    """Plot differences relative to given model_set

    parameters
    ----------
    tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    var : 'Tot' or 'Avg'
    prog_table : pd.DataFrame
    channels : [str]
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
    fig, ax = plt.subplots(len(channels), figsize=figsize, sharex=True)

    for i, channel in enumerate(channels):
        plot_summary(tables=tables,
                     column=f'{var}_{channel}',
                     x_var=x_var,
                     prog_table=prog_table,
                     x_scale=x_scale,
                     y_scale=y_scale,
                     x_lims=x_lims,
                     y_lims=y_lims,
                     marker=marker,
                     legend=False,
                     ax=ax[i])

    plt.subplots_adjust(hspace=0)
    return fig, ax


def plot_difference(tables, column, prog_table, ref_model_set,
                    x_var='m_fe',
                    x_scale=None, y_scale=None,
                    x_lims=None, y_lims=None,
                    marker='.',
                    ax=None,
                    legend=True,
                    figsize=None):
    """Plot differences relative to given model_set

    parameters
    ----------
    tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
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

    for model_set, table in tables.items():
        if model_set == ref_model_set:
            continue

        ax.plot(x, table[column] - ref_table[column],
                marker=marker, ls='none', label=model_set,
                color=config.colors.get(model_set))

    ax.hlines(0, x.min(), x.max(),
              linestyles='--',
              colors=config.colors.get(ref_model_set))

    plot_tools.set_ax_all(ax=ax, x_var=x_var, y_var=column[:3],
                          x_scale=x_scale, y_scale=y_scale,
                          x_lims=x_lims, y_lims=y_lims,
                          legend=legend)

    plt.tight_layout()
    return fig, ax


def plot_time(mass_tables, column, mass,
              x_scale=None, y_scale=None,
              ax=None, legend=True, figsize=None):
    """Plot time-dependent quantity from mass tables

    parameters
    ----------
    mass_tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
    mass : float or int
    y_scale : str
    x_scale : str
    ax : Axis
    legend : bool
    figsize : (width, height)
    """
    fig, ax = setup_fig_ax(ax=ax, figsize=figsize)

    for model_set, tables in mass_tables.items():
        table = tables[mass]
        ax.step(table['Time'], table[column],
                where='post', label=model_set,
                color=config.colors.get(model_set))

    plot_tools.set_ax_all(ax=ax, x_var='Time', y_var=column[:3],
                          x_scale=x_scale, y_scale=y_scale,
                          legend=legend)

    return fig, ax


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
