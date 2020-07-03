def create_pinched(a,m,timebins,energies,Fnu):
        """Writes input files for snowglobes in fluxes directory \n
        Creates key file to indicate how file index is related to time \n
        Creates pinched file with fluxes for every timestep \n
        Input: alpha, mass, timebins for snowglobes [s], energies for neutrino \n
        spectra [s], list of neutrino fluxes [GeV/s/cm^2]."""

        dt = timebins[1] - timebins[0]
        keyfile = open("./fluxes/pinched_a"+str(a)+"_m"+str(m)+"_key.dat","w")
        keyfile.write("### i \t time(s) \t dt(s) \n")
        for i in range(len(timebins)):
            keyfile.write(str(i+1) + "\t" + str(timebins[i]) + "\t" + str(dt) +"\n")
            outfile = open("./fluxes/pinched_a"+str(a)+"_m"+str(m)+"_"+str(i+1)+".dat","w")
            outfile.write("#### E_nu \t e \t mu \t tau \t ebar \t mubar \t taubar \n")
            for j in range(len(energies)):
                outfile.write("{0:8.4f}".format(energies[j])+"\t"+"{0:8.4e}".format(Fnu[0][i][j]) \
                        +"\t"+"{0:8.4e}".format(Fnu[2][i][j])+"\t"+"{0:8.4e}".format(Fnu[2][i][j])+"\t"\
                        +"{0:8.4e}".format(Fnu[1][i][j])+"\t"+"{0:8.4e}".format(Fnu[2][i][j])+"\t"\
                        +"{0:8.4e}".format(Fnu[2][i][j])+"\n")
        keyfile.close()
        outfile.close()
