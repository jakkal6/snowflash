import numpy as np
import pandas as pd
import xarray as xr

# snowflash
from snowflash.utils import paths

"""
Tools for handling snowglobes data
"""


# ===============================================================
#                      Load Tables
# ===============================================================
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


def load_all_counts(zams_list,
                    model_set,
                    detector,
                    mixing):
    """Load and combine binned counts for all models

    Returns : xr.Dataset

    parameters
    ----------
    zams_list : [str]
    model_set : str
    detector : str
    mixing : str
    """
    counts = []
    for j, zams in enumerate(zams_list):
        print(f'\rLoading model counts: {j+1}/{len(zams_list)}', end='')

        counts += [load_counts(zams=zams,
                               model_set=model_set,
                               detector=detector,
                               mixing=mixing)]

    print()
    counts_array = xr.concat(counts, dim='zams')
    counts_array.coords['zams'] = list(zams_list)

    counts_set = xr.Dataset(data_vars={'counts': counts_array})

    return counts_set


def load_counts(zams,
                model_set,
                detector,
                mixing):
    """Load time/energy binned counts for an individual model

    Returns : xr.DataArray

    parameters
    ----------
    zams : str
    model_set : str
    detector : str
    mixing : str
    """
    filepath = paths.snow_counts_filepath(zams=zams,
                                          model_set=model_set,
                                          detector=detector,
                                          mixing=mixing)

    print(f'Loading counts')
    counts = xr.load_dataarray(filepath)
    
    # get sum of all channels
    tot = counts.sum('channel')
    tot.coords['channel'] = 'all'
    counts = xr.concat([tot, counts], dim='channel')

    return counts


def save_model_data(data,
                    detector,
                    model_set,
                    zams,
                    mixing):
    """Save SnowModel.data to file

    parameters
    ----------
    data : xr.Dataset
    zams : str
    model_set : str
    detector : str
    mixing : str
    """
    filepath = paths.snow_model_data_filepath(zams=zams,
                                              model_set=model_set,
                                              detector=detector,
                                              mixing=mixing)
    data.to_netcdf(filepath)


def load_model_data(detector,
                    model_set,
                    zams,
                    mixing):
    """Save SnowModel.data to file

    parameters
    ----------
    zams : str
    model_set : str
    detector : str
    mixing : str
    """
    print('Loading dataset')
    filepath = paths.snow_model_data_filepath(zams=zams,
                                              model_set=model_set,
                                              detector=detector,
                                              mixing=mixing)
    return xr.load_dataset(filepath)


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
    filepath = paths.snow_timebin_filepath(zams=zams,
                                           model_set=model_set,
                                           detector=detector,
                                           mixing=mixing)

    table = pd.read_csv(filepath, delim_whitespace=True)
    
    return table


def load_prog_table(model_set):
    """Load progenitor data table

    Returns : pd.DataFrame

    parameters
    ----------
    model_set : str
    """
    filepath = paths.prog_filepath(model_set)
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


def get_cumulative(counts):
    """Calculate cumulative neutrino counts for each time bin

    Returns : xr.DataArray

    parameters
    ----------
    counts : xr.DataArray
    """
    integrated = counts.copy()
    integrated[:] = 0

    integrated[0] = counts[0]
    for i in range(1, len(counts)):
        integrated[i] = integrated[i-1] + counts[i]

    return integrated


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


def y_column(y_var, channel):
    """Return name of column

    Returns str

    Parameters
    ----------
    y_var : 'counts' or 'energy'
    channel : str
    """
    return f'{y_var}_{channel}'
