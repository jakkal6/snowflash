import os
import shutil


def clean_model():
    """Clean up snowglobes input and output files
    """
    dirs = ['fluxes', 'out']

    for d in dirs:
        clear_dir(f'./{d}')


def clean_all():
    """Clean working directory of all temporary files
    """
    rm_dirs = ['fluxes', 'out', 'channels', 'backgrounds', 'bin',
               'smear', 'xscns', 'effic', 'glb', 'src']

    rm_files = ['supernova.pl', 'supernova.glb',
                'detector_configurations.dat', 'make_event_table.pl']

    # Delete directories
    for d in rm_dirs:
        shutil.rmtree(f'./{d}', ignore_errors=True)

    # Delete files
    for f in rm_files:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass


def clear_dir(path):
    """Delete all files within a directory

    Parameters
    ----------
    path : str
    """
    files = os.listdir(path)
    for file in files:
        os.remove(f"{path}/" + file)


if __name__ == '__main__':
    clean_all()
