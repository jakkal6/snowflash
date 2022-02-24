import os
import shutil


def mass():
    """Removes snowglobes input files from fluxes directory \n
    Output: None
    """
    clear_dir('./fluxes')
    clear_dir('./out')


def final():
    """Cleans up working directory once script is done running \n
    Removes all of the copies of the working snowglobes installation \n
    Input: None \n
    Output: None
    """
    shutil.rmtree("./fluxes")
    shutil.rmtree("./out")
    shutil.rmtree("./channels")
    shutil.rmtree("./backgrounds")
    shutil.rmtree("./bin")
    shutil.rmtree("./smear")
    shutil.rmtree("./xscns")
    shutil.rmtree("./effic")
    shutil.rmtree("./glb")
    shutil.rmtree("./src")
    os.remove("supernova.pl")
    os.remove("detector_configurations.dat")
    os.remove("make_event_table.pl")


def clear_dir(path):
    """Deletes all files within a dir (leaves the dir itself)
    """
    files = os.listdir(path)
    for file in files:
        os.remove(f"{path}/" + file)
