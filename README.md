# snowglobes

This package is for handling and plotting output data from SnowGlobes.

The main class is `SnowGlobesData` in `snowglobes.py`

## Model Sets
1. `LMP`: "Langanka Martinez-Pinedo"
    - Microphysical, NSE
    - previously labelled `aprox`
2. `LMP+N50`: LMP with updated N=50 rates based on lab measurements
     - previously labelled `lab`
3. `SNA`: Single Nucleus Approximation 
    - Bruenn 1985
     - previously labelled `noWeakRates`