import os
import numpy as np
from astropy import units


def open_tot_file(tab, output, detector, channel_groups):
    """Opens file to write out time-integrated quantities
    Returns : open file
        for writing time-integrated quantities

    Parameters
    ----------
    tab : int
    output : str
        output directory
    detector : str
        name of detector, e.g. 'ar40kt'
    channel_groups : {}
    """
    header = 'Mass\t'

    header += 'Avg_Total\t'
    for group in channel_groups:
        header += f'Avg_{group}\t'

    header += 'Tot_Total\t'
    for group in channel_groups:
        header += f'Tot_{group}\t'

    header += '\n'
    # TODO: replacee `a` with `tab`
    filepath = os.path.join(output, f'{detector}_analysis_a{tab}.dat')
    tot_file = open(filepath, "w")
    tot_file.write(header)

    return tot_file


# TODO: add args time_start, time_end
def flash_input(dat_filepath):
    """Read in FLASH data from .dat file

    Returns : time [s], lum [GeV/s], avg [GeV], rms [GeV]
        shape (n_steps, flavors)
        flavors: 0: electron, 1: anti-electron, 2: nux

    Parameters
    ----------
    dat_filepath : path to FLASH data file
    """
    cols = [0, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41]

    dat = np.loadtxt(dat_filepath, usecols=cols)

    time = dat[:, 0]
    rshock = dat[:, 1]

    start_i, bounce_i, end_i = get_slice_idxs(time=time, rshock=rshock)
    bounce_time = dat[bounce_i, 0]
    sliced = dat[start_i:end_i]

    time = sliced[:, 0] - bounce_time
    lum = sliced[:, 2:5] * 1e51 * units.erg.to(units.GeV)  # GeV/s
    avg = sliced[:, 5:8] / 1000  # GeV
    rms = sliced[:, 8:11] / 1000  # GeV

    lum[:, 2] /= 4.  # divide nu_x equally between mu, tau, mu_bar, tau_bar

    return time, lum, avg, rms


def get_slice_idxs(time, rshock,
                   rshock_max=1.29e9,
                   time_start=-0.0,
                   time_max=1.0
                   ):
    """Get start/end indexes

    Parameters
    ----------
    time : []
    rshock : []
    rshock_max : float
    time_start : float
    time_max : float
    """
    n_steps = len(time)
    start_i = 0
    bounce_i = 0
    end_i = n_steps - 1

    # find bounce idx
    for i in range(n_steps):
        if rshock[i] > 0.0:
            bounce_i = i
            break

    bounce_time = time[bounce_i]

    # find starting time before bounce
    for i in range(n_steps):
        if time[i] > bounce_time + time_start:
            start_i = i - 1
            break

    # find end idx
    for i in range(start_i, n_steps):
        if rshock[i] > rshock_max:
            end_i = i
            break
        elif time[i] - bounce_time > time_max:
            end_i = i + 1
            break

    return start_i, bounce_i, end_i
