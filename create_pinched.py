import numpy as np
import pandas as pd
import os


def write_pinched(tab, mass, timebins, e_bins, fluxes):
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
    key_filepath = os.path.join(path, f'pinched_a{tab}_m{mass}_key.dat')

    with open(key_filepath, 'w') as keyfile:
        keyfile.write("### i \t time(s) \t dt(s) \n")

        for i in range(len(timebins)):
            keyfile.write(str(i+1) + "\t" + str(timebins[i]) + "\t" + str(dt) +"\n")

            out_filepath = os.path.join(path, f'pinched_a{tab}_m{mass}_{i+1}.dat')
            table = format_table(time_i=i, e_bins=e_bins, fluxes=fluxes)
            out_str = table.to_string(justify='left', index=False)

            with open(out_filepath, 'w') as outfile:
                outfile.write(out_str)


def format_table(time_i, e_bins, fluxes):
    """Format fluxes into table

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
    table['E_nu'] = e_bins

    for flavor, key in flavor_map.items():
        table[flavor] = fluxes[key][time_i]

    return table
