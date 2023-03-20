import os


def run(model_set, mass, t_bins, material, detector):
    """Runs snowglobes on generated 'pinched' files

    Parameters
    ----------
    model_set : str
    mass : float
    t_bins : []
    material : str
    detector : str
    """
    for n in range(len(t_bins)):
        input_file = f'pinched_{model_set}_m{mass}_{n + 1}'
        run_str = f'./supernova.pl {input_file} {material} {detector}'
        os.system(run_str)
