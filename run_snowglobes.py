import os


def run(tab, mass, timebins, material, detector):
    """Runs snowglobes on generated 'pinched' files

    Parameters
    ----------
    tab : int
    mass : float
    timebins : []
    material : str
    detector : str
    """
    for n in range(len(timebins)):
        input_file = f'pinched_a{tab}_m{mass}_{n+1}'
        run_str = f'./supernova.pl {input_file} {material} {detector}'
        os.system(run_str)
