import os
import shutil

def mass(a,m):
    """Removes snowglobes input files from fluxes directory \n
       Input: alpha, mass, timebins of snowglobes data \n
       Output: None """

    files = os.listdir("./fluxes")
    for file in files:
        os.remove("./fluxes/"+file)


def alpha(nomix_tot):
    """Closes file for output of time-integrated neutrino spectra quantities \n
    Input: None \n
    Output: None """

    nomix_tot.close()

def final():
    """Cleans up working directory once script is done running \n
    Removes all of the copies of the working snowglobes installation \n
    Input: None \n
    Output: None """

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
