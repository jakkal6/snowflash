import os
import numpy as np
import pandas as pd
import xarray as xr
import ast
from configparser import ConfigParser

"""
Tools for handling snowglobes data
"""


# ===============================================================
#                      Load Tables
# ===============================================================
def load_integrated_table(model_set,
                          detector,
                          time_integral=30):
    """Load time-integrated table containing all models

    Returns : pd.DataFrame

    parameters
    ----------
    model_set : str
    detector : str
    time_integral : int
        time integrated over post-bounce (milliseconds)
    """
    path = data_path()
    filename = f'{detector}_analysis_{model_set}_{time_integral}ms.dat'
    filepath = os.path.join(path, filename)

    return pd.read_csv(filepath, delim_whitespace=True)


def load_all_timebin_tables(zams_list,
                            model_set,
                            detector,
                            mixing):
    """Load and combine timebinned tables for all models

    Returns : xr.Dataset
        3D table with dimensions (zams, n_bins)

    parameters
    ----------
    zams_list : [str]
    model_set : str
    detector : str
    mixing : str
    """
    tables_dict = {}
    for j, zams in enumerate(zams_list):
        print(f'\rLoading timebin tables: {j+1}/{len(zams_list)}', end='')

        table = load_timebin_table(zams=zams,
                                   model_set=model_set,
                                   detector=detector,
                                   mixing=mixing)

        table.set_index('time', inplace=True)
        tables_dict[zams] = table.to_xarray()

    print()
    timebin_tables = xr.concat(tables_dict.values(), dim='zams')
    timebin_tables.coords['zams'] = list(zams_list)

    return timebin_tables


def load_timebin_table(zams,
                       model_set,
                       detector,
                       mixing):
    """Load timebinned table for an individual model

    Returns : pd.DataFrame

    parameters
    ----------
    zams : str
    model_set : str
    detector : str
    mixing : str
    """
    path = model_path(model_set=model_set, detector=detector, mixing=mixing)
    filename = f'timebin_{detector}_{mixing}_{model_set}_m{zams}.dat'

    filepath = os.path.join(path, filename)
    table = pd.read_csv(filepath, delim_whitespace=True)
    
    return table


def load_prog_table(model_set):
    """Load progenitor data table

    Returns : pd.DataFrame

    parameters
    ----------
    model_set : str
    """
    filepath = prog_path(model_set)
    table = pd.read_csv(filepath)

    return table


# ===============================================================
#                      Analysis
# ===============================================================
def time_integrate(timebin_tables, n_bins, channels):
    """Integrate a set of models over a given no. of time bins

    Returns : xr.Dataset
        dim: [zams]

    parameters
    ----------
    timebin_tables : xr.Dataset
        3D table of timebinned models, dim: [zams, time]
    n_bins : int
        no. of time bins to integrate over. Currently each bin is 5 ms
    channels : [str]
        list of channel names
    """
    channels = ['total'] + channels

    time_slice = timebin_tables.isel(time=slice(0, n_bins))
    totals = time_slice.sum(dim='time')
    table = xr.Dataset()

    for channel in channels:
        tot = f'counts_{channel}'
        avg = f'energy_{channel}'

        total_counts = totals[tot]
        total_energy = (time_slice[avg] * time_slice[tot]).sum(dim='time')

        table[tot] = total_counts
        table[avg] = total_energy / total_counts

    return table


def get_cumulative(timebin_tables, max_n_bins, channels):
    """Calculate cumulative neutrino counts for each time bin

    Returns : xr.Dataset
        3D table with dimensions (zams, n_bins)

    parameters
    ----------
    timebin_tables : {zams: pd.DataFrame}
        collection of timebinned model tables
    max_n_bins : int
        maximum time bins to integrate up to
    channels : [str]
        list of channel names
    """
    bins = np.arange(1, max_n_bins+1)
    cumulative = {}

    for b in bins:
        print(f'\rIntegrating bins: {b}/{max_n_bins}', end='')
        cumulative[b] = time_integrate(timebin_tables, n_bins=b, channels=channels)

    print()
    x = xr.concat(cumulative.values(), dim='time')
    x.coords['time'] = np.array(timebin_tables['time'])[1:]
    
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
            fracs[i] = np.mean(table[f'counts_{channel}'] / table['counts_total'])

        frac_table[model_set] = fracs

    frac_table.index = channels
    return frac_table


# ===============================================================
#                      Paths
# ===============================================================
def data_path():
    """Return path to Snowglobes data directory

    Returns : str
    """
    path = os.path.join(top_path(), 'output')
    return path


def model_path(model_set, detector, mixing):
    """Return path to model data

    Returns : str

    parameters
    ----------
    model_set : str
    detector : str
    mixing : str
    """
    path = os.path.join(data_path(), model_set, detector, mixing)
    return path


def prog_path(model_set):
    """Return path to progenitor table

    Returns : str

    parameters
    ----------
    model_set : str
    """
    return os.path.join(data_path(), model_set, 'progenitor_table.dat')


def y_column(y_var, channel):
    """Return name of column

    Returns str

    Parameters
    ----------
    y_var : 'counts' or 'energy'
    channel : str
    """
    return f'{y_var}_{channel}'


# =======================================================
#                 Config files
# =======================================================
def load_config(config_name):
    """Load .ini config file and return as dict

    Returns : {}

    parameters
    ----------
    config_name : str
    """
    filepath = config_filepath(config_name)
    ini = ConfigParser()
    ini.read(filepath)

    config = {}
    for section in ini.sections():
        config[section] = {}

        for option in ini.options(section):
            config[section][option] = ast.literal_eval(ini.get(section, option))

    return config


def top_path():
    """Return path to top-level repo directory

    Returns : str
    """
    path = os.path.join(os.path.dirname(__file__), '..', '..')
    path = os.path.abspath(path)

    return path


def config_filepath(config_name):
    """Return path to config file

    Returns : str

    parameters
    ----------
    config_name : str
    """
    filename = f'{config_name}.ini'
    filepath = os.path.join(top_path(), 'config', filename)

    if not os.path.exists(filepath):
        filepath = os.path.join(top_path(), 'config', 'models', filename)

    filepath = os.path.abspath(filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file not found: {filepath}')

    return filepath
