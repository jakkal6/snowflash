import numpy as np
from scipy.interpolate import interp1d
from scipy import special

def phi(E_nu,E_nu0,alpha):
    """Used to calculate flux for snowglobes input \n
    Input: E_nu: neutrino energy in GeV \n
           E_nu0: neutrino average energy in GeV \n
           alpha: pinch parameter \n
    Output: phi for flux calculation"""
    N = ((alpha+1.)**(alpha+1.))/(E_nu0*special.gamma(alpha+1.))
    R = N*((E_nu/E_nu0)**(alpha))*np.exp(-1.*(alpha+1.)*E_nu/E_nu0)

    return R


def convert(time,lum,avgE,rmsE,dist):
    """Convert FLASH data to fluxes and units needed by snowglobes \n
    Input: time: in seconds from FLASH smulation \n
           lum: list of luminosities from FLASH \n
           avgE: list of average energies from FLASH \n
           rmsE: list of rms energies from FLASH \n
           dist: event distance in cm \n
    Output: timebins: time steps for snowglobes calculations in seconds \n
            energy: neutrino energy binning for snowglobes in GeV \n
            Fnu: list of fluxes for snowglobes in GeV/s/cm^2 \n
                    1: electron, 2: anti electron, 3: nux"""

    estep = 0.0002

    alpha = [[],[],[]]
    for i in range(len(time)):
        alpha[0].append((rmsE[0][i]*rmsE[0][i] - 2.0*avgE[0][i]*avgE[0][i])/(avgE[0][i]*avgE[0][i] - rmsE[0][i]*rmsE[0][i]))
        alpha[1].append((rmsE[1][i]*rmsE[1][i] - 2.0*avgE[1][i]*avgE[1][i])/(avgE[1][i]*avgE[1][i] - rmsE[1][i]*rmsE[1][i]))
        alpha[2].append((rmsE[2][i]*rmsE[2][i] - 2.0*avgE[2][i]*avgE[2][i])/(avgE[2][i]*avgE[2][i] - rmsE[2][i]*rmsE[2][i]))

    ## Convert to GeV
    avgE = np.array(avgE)/1000.0
    avgE = avgE.tolist()

    ## Convert to GeV/s
    lum = np.array(lum)*624.15
    lum[2] /= 4.
    lum = lum.tolist()

    t_start = time[0]
    t_end = time[-1]
    t_step = 0.005 ##np.log10(t_end/t_start)/float(ntimebins)
    ntimebins = int((t_end-t_start)/t_step)+1
    timebins = []
    tot_dt = 0.0
    dt = []
    for i in range(ntimebins):
        t = t_start+float(i)*t_step ##*10.0**(float(i)*t_step)
        timebins.append(t)
        dt.append(t_step) ##*(10.0**(float(i+0.5)*t_step)-10.0**(float(i-0.5)*t_step)))
        tot_dt += dt[i]

    f = interp1d(time,alpha[0])
    alpha[0] = f(timebins)
    f = interp1d(time,avgE[0])
    avgE[0] = f(timebins)
    f = interp1d(time,lum[0])
    lum[0] = f(timebins)

    alpha[1] = np.interp(timebins,time,alpha[1])
    avgE[1] = np.interp(timebins,time,avgE[1])
    lum[1] = np.interp(timebins,time,lum[1])

    alpha[2] = np.interp(timebins,time,alpha[2])
    avgE[2] = np.interp(timebins,time,avgE[2])
    lum[2] = np.interp(timebins,time,lum[2])

    F_nue = [np.zeros(501) for i in range(len(timebins))]
    F_nubar = [np.zeros(501) for i in range(len(timebins))]
    F_nux = [np.zeros(501) for i in range(len(timebins))]
    energy = np.zeros(501)
    for i in range(len(timebins)):
        E_nu = 0.0
        lum_nue = lum[0][i]*dt[i]*1.e51
        lum_nubar = lum[1][i]*dt[i]*1.e51
        lum_nux = lum[2][i]*dt[i]*1.e51
        for j in range(501):
            energy[j] = E_nu
            if avgE[0][i] > 0.0:
                F_nue[i][j] += 1./(4.*3.14*dist*dist)*lum_nue/avgE[0][i]*phi(E_nu,avgE[0][i],alpha[0][i])*estep
            else:
                F_nue[i][j] += 0.0
            if avgE[1][i] > 0.0:
                F_nubar[i][j] += 1./(4.*3.14*dist*dist)*lum_nubar/avgE[1][i]*phi(E_nu,avgE[1][i],alpha[1][i])*estep
            else:
                F_nubar[i][j] += 0.0
            if avgE[2][i] > 0.0:
                F_nux[i][j] += 1./(4.*3.14*dist*dist)*lum_nux/avgE[2][i]*phi(E_nu,avgE[2][i],alpha[2][i])*estep
            else:
                F_nux[i][j] += 0.0
            E_nu += estep

    return timebins,energy,[F_nue,F_nubar,F_nux]
