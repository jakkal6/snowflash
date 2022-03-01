# flash_snowglobes

[![DOI](https://zenodo.org/badge/342716130.svg)](https://zenodo.org/badge/latestdoi/342716130)

Tools for running [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes) on FLASH models to predict neutrino observables.

You may also be interested in [SNEWPY](https://github.com/SNEWS2/snewpy), a generalized implementation of a similar pipeline for other CCSN codes.

`flash_snowglobes` contains two modules:

## 1. flash2snowglobes
Modules to convert FLASH data to neutrino fluxes and run snowglobes.

Credit: Adapted from scripts written by [MacKenzie Warren](https://github.com/mackenzie-warren).

The main loop is `flash2snowglobes.py`, which takes FLASH input, converts it to the neutrino fluences for snowglobes, runs snowglobes on each time bin, then extracts the output. Currently defaults to 5ms time bins. The extracted output is in the form of average detected energies and neutrino counts.


## 2. snow_data

Subpackage for handling and plotting snowglobes output, as used in the electron-capture rate project.

The main class is `snow_data.SnowData`.
