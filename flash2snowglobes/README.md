# flash2snowglobes
Wrapper code for running [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes) on flash models, modified to work with the ecRateStudy models with a DUNE-like argon detector.

Credit: originally written by MacKenzie Warren

The main loop is `flash2snowglobes.py`. It will take FLASH input, convert it to the correct input for snowglobes, run snowglobes on each "time snapshot", then analyze the output of snowglobes. It currently defaults to time bins of 5ms, which is standard time resolution for these detectors. The current output is in the form of average energies and number of neutrino counts.
