# flash_snowglobes

[![DOI](https://zenodo.org/badge/342716130.svg)](https://zenodo.org/badge/latestdoi/342716130)

Tools for running [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes) on FLASH models to predict neutrino observables.

You may also want to check out [SNEWPY](https://github.com/SNEWS2/snewpy), an implementation of the SNOwGLoBES pipeline for multiple CCSN codes.

Credit: Portions are adapted from scripts written by [MacKenzie Warren](https://github.com/mackenzie-warren).

The main script is `snowglobes/flash2snowglobes.py`, which takes FLASH output, converts it to neutrino fluences at Earth for snowglobes, runs snowglobes on each time bin, and extracts the output. 

The extracted output is in the form of average detected energies and neutrino counts.