import numpy as np
from scipy.special import gamma
from scipy.integrate import trapz


def get_fluences(time, lum, avg, rms, dist, timebins, e_bins):
    """Calculate pinched neutrino fluences at Earth for snowglobes input

    Returns: timebins, e_bins, fluxes
        timebins: time steps for snowglobes calculations in seconds
        energy: neutrino energy binning for snowglobes in GeV
        Fnu: list of fluxes for snowglobes in GeV/s/cm^2

    Parameters
    ----------
    time : [timesteps]
        timesteps from FLASH smulation [s]
    lum : [timesteps, flavor]
        list of luminosities from FLASH [GeV/s]
    avg : [timesteps, flavor]
        average energies from FLASH [GeV]
    rms : [timesteps, flavor]
        rms neutrino energies from FLASH [GeV]
    dist : float
        event distance [cm]
    timebins : []
        time bins to sample over [leftside]
    e_bins : []
        neutrino energy bins to sample [GeV]
    """
    flavors = ['e', 'a', 'x']  # nu_e, nu_ebar, nu_x

    alpha = get_alpha(avg=avg, rms=rms)

    integrated = integrate_bins(time=time,
                                alpha=alpha,
                                avg=avg,
                                lum=lum,
                                timebins=timebins,
                                flavors=flavors)

    t_binsize = np.diff(timebins)[0]
    e_binsize = np.diff(e_bins)[0]
    lum_to_flux = 1 / (4 * np.pi * dist**2)
    fluences = {f: np.zeros([len(timebins), len(e_bins)]) for f in flavors}

    for i, flav in enumerate(flavors):
        lum_f = integrated['lum'][:, i]
        mean_avg = integrated['avg'][:, i] / t_binsize
        mean_alpha = integrated['alpha'][:, i] / t_binsize

        for j, e_bin in enumerate(e_bins):
            phi = get_phi(e_bin, mean_avg, mean_alpha)
            fluences[flav][:, j] = lum_to_flux * (lum_f / mean_avg) * phi * e_binsize

    return fluences


def integrate_bins(time, alpha, avg, lum, timebins, flavors):
    """Integrate quantities into timebins

    Returns: {var: [timebins]}

    Parameters
    ----------
    time : [timesteps]
    alpha : [timesteps, flavor]
    avg : [timesteps, flavor]
    lum : [timesteps, flavor]
    timebins : []
    flavors : [str]
    """
    dt = np.diff(timebins)[0]
    n_bins = len(timebins)
    n_flavors = len(flavors)

    full_timebins = np.append(timebins, timebins[-1] + dt)
    i_bins = np.searchsorted(time, full_timebins)

    integrated = {}

    for key, quant in {'alpha': alpha, 'avg': avg, 'lum': lum}.items():
        integrated[key] = np.zeros([n_bins, n_flavors])
        y_edges = interpolate_bin_edges(time=time, timebins=timebins, y=quant)

        for i in range(n_bins):
            i_left, i_right = i_bins[i:i+2]
            x = np.array(time[i_left-1:i_right+1])
            y = np.array(quant[i_left-1:i_right+1])

            x[[0, -1]] = full_timebins[[i, i+1]]
            y[[0, -1]] = y_edges[[i, i+1]]

            integrated[key][i] = trapz(y=y, x=x, axis=0)

    return integrated


def interpolate_bin_edges(time, timebins, y):
    """Interpolate values at bin edges

    Returns: [timebins, flavors]

    Parameters
    ----------
    time : []
    timebins : []
    y : []
    """
    dt = np.diff(timebins)[0]
    full_timebins = np.append(timebins, timebins[-1] + dt)
    i_bins = np.searchsorted(time, full_timebins)

    y0 = y[i_bins-1].transpose()
    y1 = y[i_bins].transpose()

    x = full_timebins
    x0 = time[i_bins-1]
    x1 = time[i_bins]

    y_out = (y0*(x1 - x) + y1*(x - x0)) / (x1 - x0)

    return y_out.transpose()


def get_phi(e_bin, avg, alpha):
    """Calculate phi parameter

    Returns : [timesteps]
        phi parameter for flux calculation

    Parameters
    ----------
    e_bin : float
        neutrino energy bin [GeV]
    avg : [timesteps]
        average neutrino energy [GeV]
    alpha : [timesteps]
        pinch parameter
    """
    n = ((alpha + 1) ** (alpha + 1)) / (avg * gamma(alpha + 1))
    phi = n * ((e_bin / avg)**alpha) * np.exp(-(alpha + 1) * e_bin / avg)

    return phi


def get_bins(x0, x1, dx, endpoint):
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
    """
    n_bins = int((x1 - x0) / dx)

    if endpoint:
        n_bins += 1

    return np.linspace(x0, x1, num=n_bins, endpoint=endpoint)


def get_alpha(avg, rms):
    """Calculate pinch parameter from average and RMS neutrino energies

    Returns: [timesteps]

    Parameters
    ----------
    avg : [timesteps]
    rms : [timesteps]
    """
    return (rms*rms - 2.0*avg*avg) / (avg*avg - rms*rms)
