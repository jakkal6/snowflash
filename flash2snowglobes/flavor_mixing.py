

def mix_fluences(fluences, mixing):
    """Mix neutrino flavors for MSW oscillations
        See also:
            - Dighe & Smirnov (2000),
            - Nagakura et al. (2021)

    Returns: fluence_mix {flavor: [t_bins, e_bins]}

    Parameters
    ----------
    fluences : {flavor: [t_bins, e_bins]}
    mixing : 'normal', 'inverted', or 'none'
    """
    fluence_mix = {}
    p, pbar = mixing_fractions(mixing=mixing)

    # Note: input heavy flavor x=xbar is assumed
    fluence_mix['e'] = p*fluences['e'] + (1 - p)*fluences['x']
    fluence_mix['a'] = pbar*fluences['a'] + (1 - pbar)*fluences['x']
    fluence_mix['x'] = 0.5*(1 - p)*fluences['e'] + 0.5*(1 + p)*fluences['x']
    fluence_mix['ax'] = 0.5*(1 - pbar)*fluences['a'] + 0.5*(1 + pbar)*fluences['x']

    return fluence_mix


def mixing_fractions(mixing):
    """Return mixing parameters

    Returns: p, pbar

    Parameters
    ----------
    mixing : 'normal', 'inverted', or 'none'
    """
    # Capozzi et al. (2017)
    sin2_12 = 0.297
    sin2_13 = 0.0215

    p = 1.0
    pbar = 1.0

    if mixing == "normal":
        print('Using normal mixing')
        p = sin2_13
        pbar = (1 - sin2_12) * (1 - sin2_13)

    elif mixing == "inverted":
        print('Using inverted mixing')
        p = sin2_12 * (1 - sin2_13)
        pbar = sin2_13

    elif mixing == 'nomix':
        print('Using no mixing')

    else:
        raise ValueError("mixing must be one of ['normal', 'inverted', 'nomix']")
    
    return p, pbar
