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
    filename = f'{detector}_analysis_a{alpha}.dat'
    filepath = os.path.join('../SnowglobesData', filename)
    return pd.read_csv(filepath, delim_whitespace=True)


def load_mass_table(mass, alpha, detector):
    """Load time-binned table for an individual mass model

    parameters
    ----------
    mass : str
    alpha : int
    detector : str
    """
    filename = f'{detector}_analysis_a{alpha}_m{mass}.dat'
    filepath = os.path.join('../SnowglobesData', 'output', filename)
    return pd.read_csv(filepath, delim_whitespace=True)
