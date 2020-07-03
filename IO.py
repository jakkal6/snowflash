import numpy as np

def total_files(a,output):
    """Opens file to write out time-integrated quantities \n
    Input: alpha value, output path directory \n
    Output: file for time-integrated quantities to be used in analysis"""

    nomix_tot = open(output+"/nomix_analysis_a"+str(a)+".dat","w")
    nomix_tot.write("Mass \t Total \t IBD \t ES \t nu_e-O16 \t anu_e-O16 \t NC \n")
    return nomix_tot

def input(datafile):
    """Read in FLASH data from .dat file \n
    Currently using data from bounce to 1s post-bounce, with check that \n
    shock radius doesn't leave domain. \n
    Input: path to FLASH data file \n
    Output: time, list of luminosities, list of average energies, \n
    list of rms energies
    Lists indexed by flavor: 1: electron, 2: anti electron, 3: nux"""

    time,rad,lum_nue,lum_nubar,lum_nux,avgE_nue,avgE_nubar,avgE_nux,rms_nue,rms_nubar,rms_nux \
            = np.loadtxt(datafile,usecols=(0,11,33,34,35,36,37,38,39,40,41), unpack=True)

    for i in range(len(time)):
        t = time[i]
        if rad[i] > 0.0:
            bo = i
            break
    for j in range (1,len(time)):
        t = time[j]
        e = len(time)-1
        if rad[j] > 1.29e9:
            e = j
            break
        if time[j] - time[bo] > 1.0:
            e = j
            break
    time = time[bo:e]-time[bo]
    rad = rad[bo:e]
    lum_nue = lum_nue[bo:e]
    lum_nubar = lum_nubar[bo:e]
    lum_nux = lum_nux[bo:e]
    avgE_nue = avgE_nue[bo:e]
    avgE_nubar = avgE_nubar[bo:e]
    avgE_nux = avgE_nux[bo:e]
    rms_nue = rms_nue[bo:e]
    rms_nubar = rms_nubar[bo:e]
    rms_nux = rms_nux[bo:e]

    return time,[lum_nue,lum_nubar,lum_nux],[avgE_nue,avgE_nubar,avgE_nux], \
            [rms_nue,rms_nubar,rms_nux]
