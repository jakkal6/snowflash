import os


def top_path():
    """Return path to top-level repo directory

    Returns : str
    """
    path = os.path.join(os.path.dirname(__file__), '..', '..')
    path = os.path.abspath(path)

    return path


def config_filepath(name):
    """Return path to config file

    Returns : str

    parameters
    ----------
    name : str
    """
    filename = f'{name}.ini'
    filepath = os.path.join(top_path(), 'config', filename)

    if not os.path.exists(filepath):
        filepath = os.path.join(top_path(), 'config', 'models', filename)

    filepath = os.path.abspath(filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file not found: {filepath}')

    return filepath


# ===============================================================
#                          FLASH files
# ===============================================================
def dat_filepath(models_path, model_set, zams, run=None):
    """Return .dat filename

    Returns : str

    Parameters
    ----------
    models_path : str
    model_set : str
    zams : str
    run : str
        file basename (optional)
    """
    if run is None:
        filename = f'stir_ecrates_{model_set}_s{zams}_alpha1.25.dat'
    else:
        filename = f'{run}.dat'

    model_dir = f'run_{zams}'
    filepath = os.path.join(models_path, model_set, model_dir, filename)

    return filepath


def prog_filepath(model_set):
    """Return path to progenitor table

    Returns : str

    parameters
    ----------
    model_set : str
    """
    return os.path.join(output_path(), model_set, 'progenitor_table.dat')


# ===============================================================
#                          Snowglobes files
# ===============================================================
def output_path():
    """Return path to Snowglobes output

    Returns : str
    """
    return os.path.join(top_path(), 'output')


def snow_model_path(model_set, detector, mixing):
    """Return path to snowglobes model data

    Returns : str

    parameters
    ----------
    model_set : str
    detector : str
    mixing : str
    """
    return os.path.join(output_path(), model_set, detector, mixing)


def snow_timebin_filepath(zams, model_set, detector, mixing):
    """Return path to timebin file

    Returns : str

    parameters
    ----------
    zams :str
    model_set : str
    detector : str
    mixing : str
    """
    model_path = snow_model_path(model_set=model_set, detector=detector, mixing=mixing)
    filename = f'timebin_{detector}_{mixing}_{model_set}_m{zams}.dat'
    filepath = os.path.join(model_path, filename)

    return filepath


def snow_channel_dat_filepath(channel, i, model_set, zams, detector):
    """Return filepath to snowglobes output file

    Parameters
    ----------
    channel : str
    i : int
    model_set : str
    zams : str, int or float
    detector : str
    """
    filename = f'pinched_{model_set}_m{zams}_{i}_{channel}_{detector}_events_smeared.dat'
    filepath = os.path.join('./out', filename)

    return filepath


def snow_channel_dat_key_filepath(zams, model_set):
    """Return filepath to snowglobes key file

    Parameters
    ----------
    zams : str, int or float
    model_set : str
    """
    return os.path.join('./fluxes', f'pinched_{model_set}_m{zams}_key.dat')


def snow_fluence_filepath(i, zams, model_set):
    """Return filepath to snowglobes fluence input file

    Parameters
    ----------
    i : int
    zams : str, int or float
    model_set : str
    """
    filename = f'pinched_{model_set}_m{zams}_{i}.dat'
    filepath = os.path.join('./fluxes', filename)

    return filepath
