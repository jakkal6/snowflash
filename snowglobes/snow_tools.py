import os
import numpy as np
import pandas as pd

"""
Tools for handling snowglobes data
"""


# ===============================================================
#                      Load Tables
# ===============================================================
def load_summary_table(alpha, detector, time_integral=30):
    """Load time-integrated summary table containing all mass models

    Returns : pd.DataFrame

    parameters
    ----------
    alpha : int
    detector : str
    time_integral : int
        time integrated over post-bounce (milliseconds)
    """
    path = data_path()
    filename = f'{detector}_analysis_{time_integral}ms_a{alpha}.dat'
    filepath = os.path.join(path, filename)
    return pd.read_csv(filepath, delim_whitespace=True)


def load_mass_table(mass, alpha, detector):
    """Load time-binned table for an individual mass model

    Returns : pd.DataFrame

    parameters
    ----------
    mass : str
    alpha : int
    detector : str
    """
    path = data_path()
    filename = f'{detector}_analysis_a{alpha}_m{mass}.dat'
    filepath = os.path.join(path, 'mass_tables', filename)
    return pd.read_csv(filepath, delim_whitespace=True)


def load_prog_table():
    """Load progenitor data table

    Returns : pd.DataFrame
    """
    filepath = prog_path()
    return pd.read_csv(filepath, delim_whitespace=True)


# ===============================================================
#                      Analysis
# ===============================================================
def time_integrate(mass_tables, n_bins, channels):
    """Integrate a set of models over a given no. of time bins

    Returns : pd.DataFrame

    parameters
    ----------
    mass_tables : {mass: pd.DataFrame}
        collection of time-binned mass model tables
    n_bins : int
        no. of time bins to integrate over. Currently each bin is 5 ms
    channels : [str]
        list of channel labels
    """
    channels = ['Total'] + channels
    mass_list = list(mass_tables.keys())
    n_models = len(mass_list)

    mass_arrays = {}
    for channel in channels:
        mass_arrays[f'Avg_{channel}'] = np.zeros(n_models)
        mass_arrays[f'Tot_{channel}'] = np.zeros(n_models)

    # Fill mass arrays
    for i, mass in enumerate(mass_list):
        m_table = mass_tables[mass][:n_bins]
        tot = m_table.sum()

        for channel in channels:
            tot_key = f'Tot_{channel}'
            avg_key = f'Avg_{channel}'

            mass_arrays[tot_key][i] = tot[tot_key]
            mass_arrays[avg_key][i] = np.sum(m_table[avg_key] * m_table[tot_key]) / tot[tot_key]

    # Build final table from mass arrays
    table_out = pd.DataFrame()
    table_out['Mass'] = mass_list

    for column in mass_arrays.keys():
        table_out[column] = mass_arrays[column]

    return table_out


# ===============================================================
#                      Paths
# ===============================================================
def ecrate_path():
    """Return path to ecRateStudy repo

    Returns : str
    """
    try:
        path = os.environ['ECRATE']
    except KeyError:
        raise EnvironmentError('Environment variable ECRATE not set. '
                               'Set path to ecRateStudy directory, e.g. '
                               '"export ECRATE=${HOME}/projects/ecRateStudy"')
    return path


def data_path():
    """Return path to Snowglobes data

    Returns : str
    """
    path = ecrate_path()
    return os.path.join(path, 'plotRoutines', 'SnowglobesData')


def prog_path():
    """Return path to progenitor table

    Returns : str
    """
    path = ecrate_path()
    return os.path.join(path, 'plotRoutines', 'data', 'progenitor_table.dat')
