import numpy as np
import xarray as xr
from scipy.special import gamma
from scipy.integrate import trapz

"""
Note on docstrings:
    array parameters are specified by shape.
    e.g. [timesteps, flavors] --> array of shape [len(timesteps), len(flavors)]
"""


def fluences_to_xarray(fluences, t_bins, e_bins):
    """Construct DataArray from fluences dict

    Returns: xr.DataArray
    Parameters
    ----------
    fluences : {flav: [t_bins, e_bins]}
    t_bins : []
    e_bins : []
    """
    x_arrays = {}

    for flav, array in fluences.items():
        x_arrays[flav] = xr.DataArray(array,
                                      coords=[t_bins, e_bins],
                                      dims=['time', 'energy'])

    fx = xr.concat(x_arrays.values(), dim='flav')
    fx.coords['flav'] = list(x_arrays.keys())

    return fx


def calc_fluences(time, lum, avg, rms, distance, t_bins, e_bins):
    """Calculate pinched neutrino fluences at Earth for snowglobes input

    Returns: xr.DataArray

    Parameters
    ----------
    time : [timesteps]
        timesteps from FLASH smulation [s]
    lum : [timesteps, flavors]
        list of luminosities from FLASH [GeV/s]
    avg : [timesteps, flavors]
        average energies from FLASH [GeV]
    rms : [timesteps, flavors]
        rms neutrino energies from FLASH [GeV]
    distance : float
        event distance [cm]
    t_bins : [t_bins]
        time bins to sample over [leftside]
    e_bins : [e_bins]
        neutrino energy bins to sample [GeV]
    """
    print('Calculating neutrino fluences')
    flavors = ['e', 'eb', 'x']  # nu_e, nu_ebar, nu_x

    n_timebins = len(t_bins)
    n_ebins = len(e_bins)

    t_step = np.diff(t_bins)[0]
    full_timebins = np.append(t_bins, t_bins[-1] + t_step)

    flu_dict = {f: np.zeros([n_timebins, n_ebins]) for f in flavors}

    for i in range(n_timebins):
        bin_edges = full_timebins[[i, i+1]]

        t_sliced, y_sliced = slice_timebin(bin_edges=bin_edges,
                                           time=time,
                                           y_vars={'lum': lum, 'avg': avg, 'rms': rms})

        flux_spectrum = get_flux_spectrum(e_bins,
                                          lum=y_sliced['lum'],
                                          avg=y_sliced['avg'],
                                          rms=y_sliced['rms'],
                                          distance=distance)

        fluence = trapz(flux_spectrum, x=t_sliced, axis=0)

        for j, flav in enumerate(flavors):
            flu_dict[flav][i, :] = fluence[j, :]

    fluences = fluences_to_xarray(flu_dict, t_bins=t_bins, e_bins=e_bins)

    return fluences


def slice_timebin(bin_edges, time, y_vars):
    """Slice raw timesteps into a single timebin

    Returns: time, y_vars

    Parameters
    ----------
    bin_edges : [t_left, t_right]
    time: [timesteps]
    y_vars: {var: [timesteps, flavors]}
    """
    i_left, i_right = np.searchsorted(time, bin_edges)

    t_sliced = np.array(time[i_left-1:i_right+1])
    t_sliced[[0, -1]] = bin_edges  # replace endpoints with bin edges

    y_sliced = {}
    for var, values in y_vars.items():
        y_sliced[var] = np.array(values[i_left-1:i_right+1])

        # replace endpoints with exact bin edges
        y_edges = interpolate_time(t=bin_edges, time=time, y_var=values)
        y_sliced[var][[0, -1]] = y_edges

    return t_sliced, y_sliced


def get_flux_spectrum(e_bins, lum, avg, rms, distance):
    """Calculate pinched flux spectrum

    Returns: [timesteps, flavors, e_bins]
        neutrino flux at Earth (neutrinos per second) for each energy bin
        at each timepoint

    Parameters
    ----------
    e_bins : [e_bins]
    lum : [timesteps, flavors]
    avg : [timesteps, flavors]
    rms : [timesteps, flavors]
    distance : float
    """
    n_ebins = len(e_bins)
    n_time, n_flavors = lum.shape
    e_binsize = np.diff(e_bins)[0]

    flux_spectrum = np.zeros([n_time, n_flavors, n_ebins])
    alpha = get_alpha(avg=avg, rms=rms)
    lum_to_flux = 1 / (4 * np.pi * distance**2)

    for i, e_bin in enumerate(e_bins):
        phi = get_phi(e_bin=e_bin, avg=avg, alpha=alpha)
        flux_spectrum[:, :, i] = lum_to_flux * (lum / avg) * phi * e_binsize

    return flux_spectrum


def get_alpha(avg, rms):
    """Calculate pinch parameter from average and RMS neutrino energies

    Returns: [timesteps, flavors]

    Parameters
    ----------
    avg : [timesteps, flavors]
    rms : [timesteps, flavors]
    """
    return (rms**2 - 2.0*avg**2) / (avg**2 - rms**2)


def get_phi(e_bin, avg, alpha):
    """Calculate phi spectral parameter

    Returns : [timesteps, flavors]
        phi parameter for flux calculation

    Parameters
    ----------
    e_bin : float
        neutrino energy bin [GeV]
    avg : [timesteps, flavors]
        average neutrino energy [GeV]
    alpha : [timesteps, flavors]
        pinch parameter
    """
    n = ((alpha + 1) ** (alpha + 1)) / (avg * gamma(alpha + 1))
    phi = n * ((e_bin / avg)**alpha) * np.exp(-(alpha + 1) * e_bin / avg)

    return phi


def interpolate_time(t, time, y_var):
    """Linearly-interpolate values at given time points

    Returns: [t_bins, flavors]

    Parameters
    ----------
    t : []
        time points to interpolate to
    time : [timesteps]
        original time points
    y_var : [timesteps]
        data values at original time points
    """
    i_right = np.searchsorted(time, t)  # index of nearest point to the right
    i_left = i_right - 1

    y0 = y_var[i_left].transpose()
    y1 = y_var[i_right].transpose()

    t0 = time[i_left]
    t1 = time[i_right]

    y_out = (y0*(t1 - t) + y1*(t - t0)) / (t1 - t0)

    return y_out.transpose()


def get_bins(x0, x1, dx, endpoint, decimals=5):
    """Divide x into dx-spaced bins

    Returns: []

    Parameters
    ----------
    x0 : float
        lower boundary
    x1 : float
        upper boundary
    dx : float
        bin size
    endpoint : bool
        whether to include endpoint
    decimals : int
        number of decimals to round to
    """
    n_bins = round((x1 - x0) / dx)

    if endpoint:
        n_bins += 1

    bins = np.linspace(x0, x1, num=n_bins, endpoint=endpoint)
    bins = np.round(bins, decimals)

    return bins
