import numpy as np
from scipy import special


def get_fluxes(time, lum, avg, rms, dist, timebins, e_bins):
    """Calculate pinched neutrino fluxes at Earth for snowglobes input

    Returns: timebins, e_bins, fluxes
        timebins: time steps for snowglobes calculations in seconds
        energy: neutrino energy binning for snowglobes in GeV
        Fnu: list of fluxes for snowglobes in GeV/s/cm^2

    Parameters
    ----------
    time : [n_timesteps]
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

    dt = np.diff(timebins)[0]
    estep = np.diff(e_bins)[0]

    # TODO: move later e.g. create_pinched
    lum[:, 2] /= 4.  # divide nu_x equally between mu, tau, mu_bar, tau_bar

    # interpolate onto bins
    bin_centres = timebins + 0.5*dt
    binned = {}

    for key, quant in {'alpha': alpha, 'avg': avg, 'lum': lum}.items():
        binned[key] = {}
        for i, flav in enumerate(flavors):
            binned[key][flav] = np.interp(bin_centres, time, quant[:, i])

    fluxes = {f: np.zeros([len(timebins), len(e_bins)]) for f in flavors}

    lum_to_flux = 1 / (4 * np.pi * dist**2)

    for flav in flavors:
        lum_f = binned['lum'][flav] * dt
        avg_f = binned['avg'][flav]
        alpha_f = binned['alpha'][flav]

        for i, e_bin in enumerate(e_bins):
            phi = get_phi(e_bin, avg_f, alpha_f)
            fluxes[flav][:, i] = lum_to_flux * (lum_f / avg_f) * phi * estep

    return fluxes


def get_phi(e_bin, e_avg, alpha):
    """Calculate phi parameter

    Returns : [timesteps]
        phi parameter for flux calculation

    Parameters
    ----------
    e_bin : float
        neutrino energy bin [GeV]
    e_avg : [timesteps]
        average neutrino energy [GeV]
    alpha : [timesteps]
        pinch parameter
    """
    n = ((alpha + 1) ** (alpha + 1)) / (e_avg * special.gamma(alpha + 1))
    phi = n * ((e_bin / e_avg)**alpha) * np.exp(-(alpha + 1) * e_bin / e_avg)

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
