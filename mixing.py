import numpy as np


def mixing_fractions(ordering):
    """Return mixing parameters

    Returns: p, pbar

    Parameters
    ----------
    """
    # Capozzi et al. (2017), Nagakura et al. (2021)
    sin2_12 = 0.297
    sin2_13 = 0.0215

    p = 1.0
    pbar = 1.0

    if ordering == "normal":
        print('Using normal mixing')
        p = sin2_13
        pbar = (1 - sin2_12) * (1 - sin2_13)

    elif ordering == "inverted":
        print('Using inverted mixing')
        p = sin2_12 * (1 - sin2_13)
        pbar = sin2_13

    else:
        print('Using no mixing')

    return p, pbar


def mix_fluences(fluences, ordering):
    """Mix neutrino flavors for MSW oscillations

    Returns: fluence_mix {flavor: [timebins, e_bins]}

    Parameters
    ----------
    fluences : {flavor: [timebins, e_bins]}
    ordering : 'normal', 'inverted', or 'none'
    """
    fluence_mix = {}
    p, pbar = mixing_fractions(ordering=ordering)

    # Note: input heavy flavor x=xbar is assumed
    fluence_mix['e'] = p*fluences['e'] + (1 - p)*fluences['x']
    fluence_mix['a'] = pbar*fluences['a'] + (1 - pbar)*fluences['x']
    fluence_mix['x'] = 0.5*(1 - p)*fluences['e'] + 0.5*(1 + p)*fluences['x']
    fluence_mix['ax'] = 0.5*(1 - pbar)*fluences['a'] + 0.5*(1 + pbar)*fluences['x']

    return fluence_mix
