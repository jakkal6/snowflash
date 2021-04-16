import os
import numpy as np
import pandas as pd
import xarray as xr

"""
Tools for handling snowglobes data
"""


# ===============================================================
#                      Load Tables
# ===============================================================
def load_summary_table(tab, detector, time_integral=30):
    """Load time-integrated summary table containing all mass models

    Returns : pd.DataFrame

    parameters
    ----------
    tab : int
    detector : str
    time_integral : int
        time integrated over post-bounce (milliseconds)
    """
    path = data_path()
    filename = f'{detector}_analysis_{time_integral}ms_a{tab}.dat'
    filepath = os.path.join(path, filename)
    return pd.read_csv(filepath, delim_whitespace=True)


def load_all_mass_tables(mass_list, tab, detector,
                         output_dir='mass_tables'):
    """Load and combine tables for all mass models

    Returns : xr.Dataset
        3D table with dimensions (mass, n_bins)

    parameters
    ----------
    mass_list : [str]
    tab : int
    detector : str
    output_dir : str
    """
    tables_dict = {}
    for j, mass in enumerate(mass_list):
        print(f'\rLoading mass tables: {j+1}/{len(mass_list)}', end='')

        table = load_mass_table(mass=mass,
                                tab=tab,
                                detector=detector,
                                output_dir=output_dir)

        table.set_index('Time', inplace=True)
        tables_dict[mass] = table.to_xarray()

    print()
    mass_tables = xr.concat(tables_dict.values(), dim='mass')
    mass_tables.coords['mass'] = list(mass_list)

    return mass_tables


def load_mass_table(mass, tab, detector,
                    output_dir='mass_tables'):
    """Load time-binned table for an individual mass model

    Returns : pd.DataFrame

    parameters
    ----------
    mass : str
    tab : int
    detector : str
    output_dir : str
    """
    path = data_path()
    filename = f'{detector}_analysis_tab{tab}_m{mass}.dat'
    filepath = os.path.join(path, output_dir, filename)
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
        list of channel names
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


def get_cumulative(mass_tables, max_n_bins, channels):
    """Calculate cumulative neutrino counts for each time bin

    Returns : xr.Dataset
        3D table with dimensions (Mass, n_bins)

    parameters
    ----------
    mass_tables : {mass: pd.DataFrame}
        collection of time-binned mass model tables
    max_n_bins : int
        maximum time bins to integrate up to
    channels : [str]
        list of channel names
    """
    bins = np.arange(1, max_n_bins+1)
    cumulative = {}

    for b in bins:
        print(f'\rIntegrating bins: {b}/{max_n_bins}', end='')
        integrated = time_integrate(mass_tables, n_bins=b, channels=channels)
        integrated.set_index('Mass', inplace=True)
        cumulative[b] = integrated.to_xarray()

    print()
    x = xr.concat(cumulative.values(), dim='n_bins')
    x.coords['n_bins'] = bins

    return x


def get_channel_fractions(tables, channels):
    """Calculate fractional contribution of each channel to total counts

    Returns: pd.DataFrame

    Parameters
    ----------
    tables : {model_set: pd.DataFrame}
    channels : [str]
    """
    n_channels = len(channels)
    frac_table = pd.DataFrame()

    for model_set, table in tables.items():
        fracs = np.zeros(n_channels)

        for i, channel in enumerate(channels):
            fracs[i] = np.mean(table[f'Tot_{channel}'] / table['Tot_Total'])

        frac_table[model_set] = fracs

    frac_table.index = channels
    return frac_table


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


def y_column(y_var, channel):
    """Return name of column

    Returns str

    Parameters
    ----------
    y_var : 'Tot' or 'Avg'
    channel : str
    """
    return f'{y_var}_{channel}'
