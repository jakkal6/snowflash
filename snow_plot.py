import matplotlib.pyplot as plt

# snowglobes
from . import plot_tools
from . import config


def plot_summary(tables, column, prog_table,
                 x_var='mass',
                 x_scale='log', y_scale='linear',
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
                          legend=legend)

    plt.tight_layout()
    return fig, ax


def plot_time(mass_tables, column, mass,
              x_scale=None, y_scale='log',
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
