import os
import xarray as xr
import numpy as np
from astropy import units
import pandas as pd

# flash_snowglobes
from flash_snowglobes.utils import paths


# =======================================================
#                 FLASH files
# =======================================================
def read_datfile(filepath, t_start, t_end):
    """Read in FLASH data from .dat file

    Returns : {time [s], lum [GeV/s], avg [GeV], rms [GeV]}
        shape (n_steps, flavors)
        flavors: 0: electron, 1: anti-electron, 2: nux

    Parameters
    ----------
    filepath : str
        path to dat file
    t_start : float
        start of time slice (relative to bounce)
    t_end : float
        end of time slice (relative to bounce)
    """
    print(f'Reading flash neutrino output: {filepath}')
    cols = [0, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41]

    dat_raw = np.loadtxt(filepath, usecols=cols)
    time = dat_raw[:, 0]
    rshock = dat_raw[:, 1]

    i_start, i_bounce, i_end = get_slice_idxs(time=time,
                                              rshock=rshock,
                                              t_start=t_start,
                                              t_end=t_end)
    bounce_time = dat_raw[i_bounce, 0]
    sliced = dat_raw[i_start:i_end]

    dat = {'time': sliced[:, 0] - bounce_time,
           'lum': sliced[:, 2:5] * 1e51 * units.erg.to(units.GeV),
           'avg': sliced[:, 5:8] / 1000,
           'rms': sliced[:, 8:11] / 1000}

    dat['lum'][:, 2] /= 4.  # divide nu_x equally between mu, tau, mu_bar, tau_bar

    return dat


def get_slice_idxs(time, rshock,
                   t_start=0.0,
                   t_end=1.0):
    """Get indexes of time slice that includes start/end times

    Returns: i_start, i_bounce, i_end

    Parameters
    ----------
    time : []
    rshock : []
    t_start : float
    t_end : float
    """
    i_bounce = np.searchsorted(rshock, 1)  # first non-zero rshock
    bounce_time = time[i_bounce]

    i_start = np.searchsorted(time, bounce_time + t_start) - 1
    i_end = np.searchsorted(time, bounce_time + t_end) + 1

    if i_start < 0:
        raise ValueError('t_start is outside simulation time')

    if i_end > len(time):
        raise ValueError('t_end is outside simulation time')

    return i_start, i_bounce, i_end


# =======================================================
#                 Fluence files
# =======================================================
def save_fluences_raw(fluences, zams, model_set):
    """Write raw fluences data to file

    Parameters
    ----------
    fluences : xr.Dataset
    model_set : str
    zams : float
    """
    filepath = paths.model_fluences_raw_filepath(model_set=model_set, zams=zams)
    paths.check_dir_exists(os.path.dirname(filepath))

    print(f'Saving raw fluence data to: {filepath}')
    fluences.to_netcdf(filepath)


def load_fluences_raw(zams, model_set):
    """Load raw fluences data from file

    Parameters
    ----------
    model_set : str
    zams : float
    """
    filepath = paths.model_fluences_raw_filepath(model_set=model_set, zams=zams)
    print(f'Loading raw fluences from: {filepath}')
    fluences = xr.load_dataarray(filepath)

    return fluences


def write_snow_fluences(model_set,
                        zams,
                        t_bins,
                        e_bins,
                        fluences):
    """Writes input files for snowglobes in fluxes directory

    Creates key file to indicate how file index is related to time
    Creates pinched file with fluences for every timestep

    Parameters
    ----------
    model_set : str
    zams : float
        progenitor zams mass
    t_bins : []
        time bins (leftside) for fluences [s]
    e_bins : []
        energy bins (leftside) for neutrino spectra [GeV]
    fluences : xr.Dataset
        neutrino fluences over all time and energy bins [GeV/s/cm^2]
    """
    t_step = np.diff(t_bins)[0]

    # write key table
    key_table = get_key_table(t_bins=t_bins, t_step=t_step)
    key_filepath = paths.snow_channel_dat_key_filepath(zams=zams, model_set=model_set)

    with open(key_filepath, 'w') as keyfile:
        key_table.to_string(keyfile, index=False)

    # write fluence files
    for i in range(len(t_bins)):
        out_filepath = paths.snow_fluence_filepath(i=i + 1, zams=zams, model_set=model_set)

        table = format_fluence_table(time_i=i,
                                     e_bins=e_bins,
                                     fluences=fluences)

        with open(out_filepath, 'w') as outfile:
            table.to_string(outfile, header=None, index=False)


def get_key_table(t_bins, t_step):
    """Return key table

    Returns : pd.DataFrame

    Parameters
    ----------
    t_bins : []
    t_step : float
    """
    table = pd.DataFrame()
    table['i'] = np.arange(len(t_bins)) + 1
    table['time[s]'] = t_bins
    table['dt[s]'] = t_step

    return table


def format_fluence_table(time_i,
                         e_bins,
                         fluences):
    """Return fluence table for given timestep

    Returns: pd.DataFrame

    Parameters
    ----------
    time_i : int
        timestep index
    e_bins : []
    fluences : {flavor: [t_bins, e_bins]}
    """
    flavor_map = {'e': 'e',
                  'mu': 'x',
                  'tau': 'x',
                  'ebar': 'a',
                  'mubar': 'ax',
                  'taubar': 'ax',
                  }
    table = pd.DataFrame()
    table['E_nu'] = e_bins

    for flavor, key in flavor_map.items():
        table[flavor] = fluences[key][time_i]

    return table
