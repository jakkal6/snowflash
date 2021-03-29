import os
import numpy as np
from astropy import units


def read_datfile(dat_filepath, t_start, t_end):
    """Read in FLASH data from .dat file

    Returns : time [s], lum [GeV/s], avg [GeV], rms [GeV]
        shape (n_steps, flavors)
        flavors: 0: electron, 1: anti-electron, 2: nux

    Parameters
    ----------
    dat_filepath : path to FLASH data file
    t_start : float
        start of time slice (relative to bounce)
    t_end : float
        end of time slice (relative to bounce)
    """
    cols = [0, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41]

    dat = np.loadtxt(dat_filepath, usecols=cols)

    time = dat[:, 0]
    rshock = dat[:, 1]

    i_start, i_bounce, i_end = get_slice_idxs(time=time,
                                              rshock=rshock,
                                              t_start=t_start,
                                              t_end=t_end)
    bounce_time = dat[i_bounce, 0]
    sliced = dat[i_start:i_end]

    time = sliced[:, 0] - bounce_time
    lum = sliced[:, 2:5] * 1e51 * units.erg.to(units.GeV)  # GeV/s
    avg = sliced[:, 5:8] / 1000  # GeV
    rms = sliced[:, 8:11] / 1000  # GeV

    lum[:, 2] /= 4.  # divide nu_x equally between mu, tau, mu_bar, tau_bar

    return time, lum, avg, rms


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

    return i_start, i_bounce, i_end
