# flash_snowglobes

Tools for running [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes) on FLASH models to predict neutrino observables.
Contains two packages:

## 1. flash2snowglobes
Modules to convert FLASH data to neutrino fluxes and run snowglobes.

Credit: Adapted from scripts written by MacKenzie Warren.

The main loop is `flash2snowglobes.py`, which takes FLASH input, converts it to the neutrino fluences for snowglobes, runs snowglobes on each time bin, then extracts the output. Currently defaults to 5ms time bins. The extracted output is in the form of average detected energies and neutrino counts.


## 2. snowglobes

Subpackage for handling and plotting snowglobes output, as used in the electron-capture rate project.

The main class is `snowglobes.SnowGlobesData`.
