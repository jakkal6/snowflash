import numpy as np
import pandas as pd
import os


def write_fluence_files(model_set,
                        mass,
                        timebins,
                        e_bins,
                        fluences_mixed):
    """Writes input files for snowglobes in fluxes directory

    Creates key file to indicate how file index is related to time
    Creates pinched file with fluences for every timestep

    Parameters
    ----------
    model_set : str
    mass : float
        progenitor mass
    timebins : []
        time bins (leftside) for fluences [s]
    e_bins : []
        energy bins (leftside) for neutrino spectra [GeV]
    fluences_mixed : {flavor: [timebins, e_bins]}
        neutrino fluences over all time and energy bins [GeV/s/cm^2]
    """
    t_step = np.diff(timebins)[0]
    path = './fluxes'

    # write key table
    key_table = get_key_table(timebins=timebins, t_step=t_step)
    key_filepath = os.path.join(path, f'pinched_{model_set}_m{mass}_key.dat')

    with open(key_filepath, 'w') as keyfile:
        key_table.to_string(keyfile, index=False)

    # write fluence files
    for i in range(len(timebins)):
        out_filepath = os.path.join(path, f'pinched_{model_set}_m{mass}_{i + 1}.dat')
        table = format_fluence_table(time_i=i,
                                     e_bins=e_bins,
                                     fluences_mixed=fluences_mixed)

        with open(out_filepath, 'w') as outfile:
            table.to_string(outfile, header=None, index=False)


def get_key_table(timebins, t_step):
    """Return key table

    Returns : pd.DataFrame

    Parameters
    ----------
    timebins : []
    t_step : float
    """
    table = pd.DataFrame()
    table['i'] = np.arange(len(timebins)) + 1
    table['time[s]'] = timebins
    table['dt[s]'] = t_step

    return table


def format_fluence_table(time_i,
                         e_bins,
                         fluences_mixed):
    """Return fluence table for given timestep

    Returns: pd.DataFrame

    Parameters
    ----------
    time_i : int
        timestep index
    e_bins : []
    fluences_mixed : {flavor: [timebins, e_bins]}
    """
    flavor_map = {'e': 'e',
                  'mu': 'x',
                  'tau': 'x',
                  'ebar': 'a',
                  'mubar': 'ax',
                  'taubar': 'ax',
                  }
    table = pd.DataFrame()
    table['E_nu'] = e_bins

    for flavor, key in flavor_map.items():
        table[flavor] = fluences_mixed[key][time_i]

    return table
