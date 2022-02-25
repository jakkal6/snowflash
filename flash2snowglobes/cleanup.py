import os
import shutil


def clean_model():
    """Clean up snowglobes input and output files
    """
    clear_dir('./fluxes')
    clear_dir('./out')


def clean_all():
    """Clean working directory of all temporary files
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
    """Delete all files within a directory
    """
    files = os.listdir(path)
    for file in files:
        os.remove(f"{path}/" + file)
