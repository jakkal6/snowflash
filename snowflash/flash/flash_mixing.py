import xarray as xr


def mix_fluences(fluences, mixing):
    """Do mixing of flunce flavors for all mixing cases

    Returns: xr.DataArray

    Parameters
    ----------
    fluences : {flav: [t_bins, e_bins]}
    mixing : [str]
        'normal', 'inverted', and/or 'nomix'
    """
    mixed = {}

    for mix in mixing:
        mixed[mix] = mix_flavors(flu_e=fluences.sel(flav='e'),
                                 flu_eb=fluences.sel(flav='eb'),
                                 flu_x=fluences.sel(flav='x'),
                                 mixing=mix)

    fmixed = mixed_to_xarray(mixed)

    return fmixed


def mix_flavors(flu_e, flu_eb, flu_x, mixing):
    """Mix neutrino flavors for MSW oscillations
        See also:
            - Dighe & Smirnov (2000),
            - Nagakura et al. (2021)

    Returns: {flavor: arraylike}

    Parameters
    ----------
    flu_e : arraylike
    flu_eb : arraylike
    flu_x : arraylike
        Note: assumed x=xb for input heavy flavor
    mixing : 'normal', 'inverted', or 'nomix'
    """
    mixed = {}
    p, pbar = mixing_fractions(mixing=mixing)

    mixed['e'] = p * flu_e + (1 - p) * flu_x
    mixed['eb'] = pbar * flu_eb + (1 - pbar)*flu_x
    mixed['x'] = 0.5 * (1 - p) * flu_e + 0.5 * (1 + p) * flu_x
    mixed['xb'] = 0.5 * (1 - pbar) * flu_eb + 0.5 * (1 + pbar) * flu_x

    return mixed


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


def mixed_to_xarray(fluences_mixed):
    """Construct xarray DataArray from mixed fluences dicts

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
