import xarray as xr


def mixed_to_xarray(fluences_mixed):
    """Construct xarray Dataset from mixed fluences dicts

    Parameters
    ----------
    fluences_mixed : {mixing: {flav: xr.DataArray}}
    """
    x_arrays = {}

    for mixing, flav in fluences_mixed.items():
        fmix = fluences_mixed[mixing]
        x_arrays[mixing] = xr.concat(fmix.values(), dim='flav')
        x_arrays[mixing].coords['flav'] = list(fmix.keys())

    fx = xr.concat(x_arrays.values(), dim='mix')
    fx.coords['mix'] = list(x_arrays.keys())

    return fx


def mix_fluences(fluences, mixing):
    """Mix neutrino flavors for MSW oscillations
        See also:
            - Dighe & Smirnov (2000),
            - Nagakura et al. (2021)

    Returns: fluence_mix {flavor: [t_bins, e_bins]}

    Parameters
    ----------
    fluences : {flavor: [t_bins, e_bins]}
    mixing : 'normal', 'inverted', or 'nomix'
    """
    fluence_mix = {}
    p, pbar = mixing_fractions(mixing=mixing)

    flu_e = fluences.sel(flav='e')
    flu_a = fluences.sel(flav='a')
    flu_x = fluences.sel(flav='x')

    # Note: assumed input heavy flavor x=xbar
    fluence_mix['e'] = p * flu_e + (1 - p) * flu_x
    fluence_mix['a'] = pbar * flu_a + (1 - pbar)*flu_x
    fluence_mix['x'] = 0.5 * (1 - p) * flu_e + 0.5 * (1 + p) * flu_x
    fluence_mix['ax'] = 0.5 * (1 - pbar) * flu_a + 0.5 * (1 + pbar) * flu_x

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
