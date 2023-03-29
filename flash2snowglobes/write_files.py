import numpy as np
import pandas as pd
import os


def write_fluence_files(model_set,
                        zams,
                        t_bins,
                        e_bins,
                        fluences_mixed):
    """Writes input files for snowglobes in fluxes directory

    Creates key file to indicate how file index is related to time
    Creates pinched file with fluences for every timestep

    Parameters
    ----------
    model_set : str
    zams : float
        progenitor zams mass
    t_bins : []
        time bins (leftside) for fluences [s]
    e_bins : []
        energy bins (leftside) for neutrino spectra [GeV]
    fluences_mixed : {flavor: [t_bins, e_bins]}
        neutrino fluences over all time and energy bins [GeV/s/cm^2]
    """
    t_step = np.diff(t_bins)[0]
    path = './fluxes'

    # write key table
    key_table = get_key_table(t_bins=t_bins, t_step=t_step)
    key_filepath = os.path.join(path, f'pinched_{model_set}_m{zams}_key.dat')

    with open(key_filepath, 'w') as keyfile:
        key_table.to_string(keyfile, index=False)

    # write fluence files
    for i in range(len(t_bins)):
        out_filepath = os.path.join(path, f'pinched_{model_set}_m{zams}_{i + 1}.dat')
        table = format_fluence_table(time_i=i,
                                     e_bins=e_bins,
                                     fluences_mixed=fluences_mixed)

        with open(out_filepath, 'w') as outfile:
            table.to_string(outfile, header=None, index=False)


def get_key_table(t_bins, t_step):
    """Return key table

    Returns : pd.DataFrame

    Parameters
    ----------
    t_bins : []
    t_step : float
    """
    table = pd.DataFrame()
    table['i'] = np.arange(len(t_bins)) + 1
    table['time[s]'] = t_bins
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
    fluences_mixed : {flavor: [t_bins, e_bins]}
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
