import os
import shutil


def copy_snowglobes(snowglobes_path):
    """Copies snowglobes installation into working directory
    Couldn't find a way around this without going into the snowglobes code
    and altering directory paths

    Parameters
    ----------
    snowglobes_path : str
        directory path to snowglobes installation
    """
    local_path = "./"

    # create local dirs
    for folder in ['output',
                   'fluxes',
                   'out']:
        fullpath = os.path.join(local_path, folder)

        if not os.path.isdir(fullpath):
            os.makedirs(fullpath)

    # copy snowglobes dirs
    for folder in ['channels',
                   'backgrounds',
                   'bin',
                   'smear',
                   'xscns',
                   'effic',
                   'glb',
                   'src']:
        src = os.path.join(snowglobes_path, folder)
        dest = os.path.join(local_path, folder)

        if os.path.isdir(dest):
            shutil.rmtree(dest)

        shutil.copytree(src, dest)

    # link files
    for filename in ['supernova.pl',
                     'detector_configurations.dat',
                     'make_event_table.pl']:
        src = os.path.join(snowglobes_path, filename)
        dest = os.path.join(local_path, filename)

        if os.path.isfile(dest):
            os.remove(dest)

        os.symlink(src, dest)
