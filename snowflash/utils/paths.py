import os

"""
Functions that return paths to files and directories

NOTE: Unless stated otherwise, all inputs/outputs are strings

Nomenclature
    - path: path str to a directory
    - filepath: path str to a specific file
"""


# ===============================================================
#                          General
# ===============================================================
def top_path():
    """Return path to top-level repo directory
    """
    path = os.path.join(os.path.dirname(__file__), '..', '..')
    path = os.path.abspath(path)

    return path


def output_path():
    """Return path to top-level output directory
    """
    return os.path.join(top_path(), 'output')


def config_filepath(name):
    """Return path to config file
    """
    filename = f'{name}.ini'
    filepath = os.path.join(top_path(), 'config', filename)

    if not os.path.exists(filepath):
        filepath = os.path.join(top_path(), 'config', 'models', filename)

    filepath = os.path.abspath(filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file not found: {filepath}')

    return filepath


def check_dir_exists(path):
    """Create directory (tree) if it doesn't exist
    """
    if not os.path.isdir(path):
        os.makedirs(path)


# ===============================================================
#                          FLASH files
# ===============================================================
def flash_dat_filepath(models_path, model_set, zams, run=None):
    """Return filepath to flash simulation .dat
    """
    if run is None:
        filename = f'stir_ecrates_{model_set}_s{zams}_alpha1.25.dat'
    else:
        filename = f'{run}.dat'

    model_dir = f'run_{zams}'
    filepath = os.path.join(models_path, model_set, model_dir, filename)

    return filepath


def prog_filepath(model_set):
    """Return filepath to progenitor table
    """
    return os.path.join(output_path(), model_set, 'progenitor_table.dat')


# ===============================================================
#                          Model set files
# ===============================================================
def model_set_path(model_set):
    """Return path to model set directory
    """
    return os.path.join(output_path(), model_set)


def model_fluences_filepath(model_set, zams, flu_type):
    """Return filepath to raw fluences

    Parameters
    ----------
    model_set : str
    zams : str
    flu_type : 'raw' or 'mixed'
    """
    path = os.path.join(model_set_path(model_set), 'fluences', flu_type)
    filename = f'fluences_{flu_type}_{model_set}_{zams}.nc'

    return os.path.join(path, filename)


# ===============================================================
#                          Snowglobes files
# ===============================================================
def snow_runtime_path():
    """Return path to temporary snowglobes runtime directory
    """
    return os.path.join(top_path(), 'snowglobes')


def snow_model_path(model_set, detector, mixing):
    """Return path to snowglobes model output directory
    """
    return os.path.join(model_set_path(model_set), detector, mixing)


def snow_timebin_filepath(zams, model_set, detector, mixing):
    """Return path to snowglobes timebin file
    """
    model_path = snow_model_path(model_set=model_set, detector=detector, mixing=mixing)
    filename = f'timebin_{detector}_{mixing}_{model_set}_m{zams}.dat'
    filepath = os.path.join(model_path, filename)

    return filepath


def snow_counts_filepath(zams, model_set, detector, mixing):
    """Return path to snowglobes counts file
    """
    model_path = snow_model_path(model_set=model_set, detector=detector, mixing=mixing)
    filename = f'counts_{detector}_{mixing}_{model_set}_m{zams}.nc'
    filepath = os.path.join(model_path, filename)

    return filepath


def snow_model_data_filepath(zams, model_set, detector, mixing):
    """Return path to snowglobes model data file
    """
    model_path = snow_model_path(model_set=model_set, detector=detector, mixing=mixing)
    filename = f'data_{detector}_{mixing}_{model_set}_{zams}.nc'
    filepath = os.path.join(model_path, filename)

    return filepath


def snow_channel_dat_filepath(channel, i, model_set, zams, detector):
    """Return filepath to snowglobes output file
    """
    runtime_path = snow_runtime_path()
    filename = f'pinched_{model_set}_m{zams}_{i}_{channel}_{detector}_events_smeared.dat'
    filepath = os.path.join(runtime_path, 'out', filename)

    return filepath


def snow_channel_dat_key_filepath(zams, model_set):
    """Return filepath to snowglobes key file
    """
    runtime_path = snow_runtime_path()
    filename = f'pinched_{model_set}_m{zams}_key.dat'
    filepath = os.path.join(runtime_path, 'fluxes', filename)

    return filepath


def snow_fluence_filepath(i, zams, model_set):
    """Return filepath to snowglobes fluence (flux) input
    """
    runtime_path = snow_runtime_path()
    filename = f'pinched_{model_set}_m{zams}_{i}.dat'
    filepath = os.path.join(runtime_path, 'fluxes', filename)

    return filepath
