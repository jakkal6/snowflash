import os
import shutil

from flash_snowglobes.utils import paths


def copy_snowglobes(snowglobes_path):
    """Copies snowglobes installation into working directory
    Couldn't find a way around this without going into the snowglobes code
    and altering directory paths

    Parameters
    ----------
    snowglobes_path : str
        directory path to snowglobes installation
    """
    runtime_path = paths.snowglobes_runtime_path()

    # create local dirs
    new_folders = ['fluxes', 'out']

    for folder in new_folders:
        fullpath = os.path.join(runtime_path, folder)

        if not os.path.isdir(fullpath):
            os.makedirs(fullpath)

    # copy snowglobes dirs
    copy_folders = ['channels', 'backgrounds', 'bin', 'smear',
                    'xscns', 'effic', 'glb', 'src']

    for folder in copy_folders:
        src = os.path.join(snowglobes_path, folder)
        dest = os.path.join(runtime_path, folder)

        if os.path.isdir(dest):
            shutil.rmtree(dest)

        shutil.copytree(src, dest)

    # link files
    ln_files = ['supernova.pl', 'detector_configurations.dat', 'make_event_table.pl']
    
    for filename in ln_files:
        src = os.path.join(snowglobes_path, filename)
        dest = os.path.join(runtime_path, filename)

        if os.path.isfile(dest):
            os.remove(dest)

        os.symlink(src, dest)
