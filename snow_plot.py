import matplotlib.pyplot as plt

# snowglobes
from . import plot_tools
from . import config


def plot_summary(tables, column,
                 marker='.', x_scale='log', y_scale='linear',
                 legend=True, figsize=None):
    """Plot quantity from summary table

    parameters
    ----------
    tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
    marker : str
    x_scale : str
    y_scale : str
    legend : bool
    figsize : (width, height)
    """
    fig, ax = plt.subplots(figsize=figsize)

    for model_set, table in tables.items():
        ax.plot(table['Mass'], table[column],
                marker=marker, ls='none', label=model_set,
                color=config.colors.get(model_set))

    plot_tools.set_ax_all(ax=ax, x_var='Mass', y_var=column[:3],
                          x_scale=x_scale, y_scale=y_scale,
                          legend=legend)

    plt.tight_layout()
    return fig, ax


def plot_time(mass_tables, column, mass,
              x_scale=None, y_scale='log',
              legend=True):
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
    legend : bool
    """
    fig, ax = plt.subplots()

    for model_set, tables in mass_tables.items():
        table = tables[mass]
        ax.step(table['Time'], table[column],
                where='post', label=model_set,
                color=config.colors.get(model_set))

    plot_tools.set_ax_all(ax=ax, x_var='Time', y_var=column[:3],
                          x_scale=x_scale, y_scale=y_scale,
                          legend=legend)

    return fig, ax
