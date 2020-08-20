import os
import pandas as pd

"""
Tools for handling snowglobes data
"""


# ===============================================================
#                      Load Tables
# ===============================================================
def load_summary_table(alpha, detector):
    """Load time-integrated summary table containing all mass models

    parameters
    ----------
    alpha : int
    detector : str
    """
    path = data_path()
    filename = f'{detector}_analysis_a{alpha}.dat'
    filepath = os.path.join(path, filename)
    return pd.read_csv(filepath, delim_whitespace=True)


def load_mass_table(mass, alpha, detector):
    """Load time-binned table for an individual mass model

    parameters
    ----------
    mass : str
    alpha : int
    detector : str
    """
    path = data_path()
    filename = f'{detector}_analysis_a{alpha}_m{mass}.dat'
    filepath = os.path.join(path, 'output', filename)
    return pd.read_csv(filepath, delim_whitespace=True)


# ===============================================================
#                      Paths
# ===============================================================
def ecrate_path():
    """Return path to ecRateStudy repo
    """
    try:
        path = os.environ['ECRATE']
    except KeyError:
        raise EnvironmentError('Environment variable ECRATE not set. '
                               'Set path to ecRateStudy directory, e.g. '
                               '"export ECRATE=${HOME}/projects/ecRateStudy"')
    return path


def data_path():
    """Return path to Snowglobes data
    """
    path = ecrate_path()
    return os.path.join(path, 'plotRoutines', 'SnowglobesData')

