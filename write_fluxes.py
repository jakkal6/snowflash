import numpy as np
import pandas as pd
import os


def write_fluxes(tab, mass, timebins, e_bins, fluxes):
    """Writes input files for snowglobes in fluxes directory

    Creates key file to indicate how file index is related to time
    Creates pinched file with fluxes for every timestep

    Parameters
    ----------
    tab : int
        table ID
    mass : float
        progenitor mass
    timebins : []
        time bins (leftside) for fluxes [s]
    e_bins : []
        energy bins (leftside) for neutrino spectra [GeV]
    fluxes : {flavor: [timebins, e_bins]}
        neutrino fluxes over all time and energy bins [GeV/s/cm^2]
    """
    dt = np.diff(timebins)[0]
    path = './fluxes'

    # write key table
    keyfile_str = key_table_str(timebins=timebins, dt=dt)
    key_filepath = os.path.join(path, f'pinched_a{tab}_m{mass}_key.dat')

    with open(key_filepath, 'w') as keyfile:
        keyfile.write(keyfile_str)

    # write flux files
    for i in range(len(timebins)):
        out_filepath = os.path.join(path, f'pinched_a{tab}_m{mass}_{i+1}.dat')
        table_str = flux_table_str(time_i=i, e_bins=e_bins, fluxes=fluxes)

        with open(out_filepath, 'w') as outfile:
            outfile.write(table_str)


def key_table_str(timebins, dt):
    """Return formatted string of key table

    Returns : str

    Parameters
    ----------
    timebins : []
    dt : float
    """
    table = pd.DataFrame()
    table['# i'] = np.arange(len(timebins)) + 1
    table['time[s]'] = timebins
    table['dt[s]'] = dt

    table_str = table.to_string(justify='left', index=False)

    return table_str


def flux_table_str(time_i, e_bins, fluxes):
    """Return formatted string of flux table for given timestep

    Returns: pd.DataFrame

    Parameters
    ----------
    time_i : int
        timestep index
    e_bins : []
    fluxes : {flavor: [timebins, e_bins]}
    """
    flavor_map = {'e': 'e',
                  'mu': 'x',
                  'tau': 'x',
                  'ebar': 'a',
                  'mubar': 'x',
                  'taubar': 'x',
                  }
    table = pd.DataFrame()
    table['# E_nu'] = e_bins

    for flavor, key in flavor_map.items():
        table[flavor] = fluxes[key][time_i]

    table_str = table.to_string(justify='left', index=False)

    return table_str
