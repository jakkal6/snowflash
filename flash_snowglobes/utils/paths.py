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
    model_dir = f'run_{zams}'
    filename = dat_filename(model_set=model_set, zams=zams, run=run)
    filepath = os.path.join(models_path, model_set, model_dir, filename)

    return filepath


def dat_filename(model_set, zams, run=None):
    """Return .dat filename

    Returns : str

    Parameters
    ----------
    model_set : str
    zams : str
    run : str
        file basename (optional)
    """
    if run is None:
        filename = f'stir_ecrates_{model_set}_s{zams}_alpha1.25.dat'
    else:
        filename = f'{run}.dat'

    return filename
