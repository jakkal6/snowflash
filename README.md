# flash2snowglobes
MacKenzie's wrapper code for running SNOwGLoBES on flash models, modified to run on the ecRateStudy models.

In his words: 

"Snowglobes is written to take a single flux versus energy snapshot as input, so getting it work with time-dependent data gets messy. Rather than rework snowglobes directly, I've basically just written a giant python wrapper for it.  
The "main loop" is the flash2snowglobes.py file. It will take FLASH input, convert it to the correct input for snowglobes, run snowglobes on each "time snapshot", then analyze the output of snowglobes. It currently defaults to time bins of 5ms, which is standard time resolution for these detectors. The current output is in the form of average energies and number of neutrino counts, but that can easily be changed to whatever you need."
