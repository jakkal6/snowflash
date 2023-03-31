import os

from flash_snowglobes.utils import paths


def run(model_set, zams, n_bins, material, detector):
    """Runs snowglobes on generated 'pinched' files

    Parameters
    ----------
    model_set : str
    zams : float
    n_bins : int
    material : str
    detector : str
    """
    runtime_path = paths.snowglobes_runtime_path()
    os.system(f'cd {runtime_path}')

    for n in range(n_bins):
        input_file = f'pinched_{model_set}_m{zams}_{n + 1}'
        run_str = f'{runtime_path}/supernova.pl {input_file} {material} {detector}'
        os.system(run_str)
