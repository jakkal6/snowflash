import os


def run(model_set, mass, timebins, material, detector):
    """Runs snowglobes on generated 'pinched' files

    Parameters
    ----------
    model_set : str
    mass : float
    timebins : []
    material : str
    detector : str
    """
    for n in range(len(timebins)):
        input_file = f'pinched_{model_set}_m{mass}_{n + 1}'
        run_str = f'./supernova.pl {input_file} {material} {detector}'
        os.system(run_str)
