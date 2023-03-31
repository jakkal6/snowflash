import numpy as np
from astropy import units


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
    print(f'Reading flash output: {filepath}')
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
