import matplotlib.pyplot as plt


def plot_summary(tables, column,
                 marker='.', xscale='log', yscale='linear'):
    """Plot quantity from summary table

    parameters
    ----------
    tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
    marker : str
    xscale : str
    yscale : str
    """
    fig, ax = plt.subplots()

    for model_set, table in tables.items():
        ax.plot(table['Mass'], table[column],
                marker=marker, ls='none', label=model_set)

    ylabel = {
        'Tot': 'counts',
        'Avg': 'avg energy (MeV)',
    }.get(column[:3])
    ax.set_ylabel(ylabel)
    ax.set_xlabel('ZAMS Mass (Msun)')
    ax.legend()
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    return fig, ax


def plot_time(mass_tables, column, mass,
              yscale='log', xfactor=1.0):
    """Plot time-dependent quantity from mass tables

    parameters
    ----------
    mass_tables : {model_set: pd.DataFrame}
        collection of summary_tables to plot
    column : str
        which column to plot
    mass : float or int
    xfactor : float
    yscale : str
    """
    fig, ax = plt.subplots()

    for model_set, tables in mass_tables.items():
        table = tables[mass]
        ax.step(table['Time']*xfactor, table[column],
                where='post', label=model_set)

    ylabel = {
        'Tot': 'counts',
        'Avg': 'avg energy (MeV)',
    }.get(column[:3])
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Time (s)')
    ax.set_xscale('symlog', linthreshx=0.1)
    ax.set_yscale(yscale)
    ax.legend()

    return fig, ax
