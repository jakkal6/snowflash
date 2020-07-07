import numpy as np

def analysis(a,m,timebins,output,detector,nomix_tot):
        """Does analysis on snowglobes output and writes out to ascii files in output \n
        Kinda a mess since it's hacked in from historical scripts \n
        Currently calculating mean energy and total counts for each detector channel \n
        for each timestep and calculating time-integrated mean energies \n
        Input: alpha, mass, timebins for snowglobes code [s], \n
        output directory path, detector configuration\n
        nomix_tot file for time-integrated quantities \n
        Output: None"""

        nomix_time = open(output+"/nomix_analysis_a"+str(a)+"_m"+str(m)+".dat","w")
        nomix_time.write("Time \t Avg_Total \t Avg_IBD \t Avg_ES \t Avg_nu_e-O16 \t Avg_anu_e-O16 \t Avg_NC \
                \t Tot_Total \t Tot_IBD \t Tot_ES \t Tot_nu_e-O16 \t Tot_anu_e-O16 \t Tot_NC \n")

        time = np.loadtxt('./fluxes/pinched_a'+str(a)+'_m'+str(m)+'_key.dat',skiprows=1,usecols=(1),unpack=True)

        nomix_ibd = np.zeros(200)
        nomix_es = np.zeros(200)
        nomix_eo16 = np.zeros(200)
        nomix_ao16 = np.zeros(200)
        nomix_nc = np.zeros(200)
        nomix_total = np.zeros(200)
        for i in range(1,len(timebins)+1):
            en1,ibd1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_ibd_'+str(detector)+'_events_smeared.dat', skip_footer = 2,usecols=(0,1), unpack=True)
            es1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nue_e_'+str(detector)+'_events_smeared.dat', skip_footer = 2,usecols=(1), unpack=True)
            eo161 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nue_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            ao161 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nuebar_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            enc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_nue_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            anc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_nuebar_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            munc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_numu_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            mubarnc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_numubar_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            taunc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_nutau_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)
            taubarnc1 = np.genfromtxt('./out/pinched_a'+str(a)+'_m'+str(m)+'_'+str(i)+'_nc_nutaubar_O16_'+str(detector)+'_events_smeared.dat',skip_footer = 2, usecols=(1), unpack=True)

            nomix_en = en1
            tot1 = ibd1 + es1 + eo161+ao161+enc1+anc1+munc1+mubarnc1+taunc1+taubarnc1
            nomix_total += tot1
            nomix_ibd += ibd1
            nomix_es += es1
            nomix_eo16 += eo161
            nomix_ao16 += ao161
            nc1 = enc1 + anc1 + munc1 + mubarnc1 + taunc1 + taubarnc1
            nomix_nc += nc1

            tot_tot = sum(tot1)
            if(sum(tot1) != 0.0 ):
              av_tot = sum(tot1*en1*1000)/sum(tot1)
            else:
              av_tot = 0.0

            tot_ibd = sum(ibd1)
            if(sum(ibd1) != 0.0 ) :
              av_ibd = sum(ibd1*en1*1000)/sum(ibd1)
            else:
              av_ibd = 0.0

            tot_es = sum(es1)
            if(sum(es1) != 0.0):
              av_es = sum(es1*en1*1000)/sum(es1)
            else:
              av_es = 0.0

            tot_eo16 = sum(eo161)
            if(sum(eo161) != 0.0):
              av_eo16 = sum(eo161*en1*1000)/sum(eo161)
            else:
              av_eo16 = 0.0

            tot_ao16 = sum(ao161)
            if(sum(ao161) != 0.0):
              av_ao16 = sum(ao161*en1*1000)/sum(ao161)
            else:
              av_ao16 = 0.0

            tot_nc = sum(nc1)
            if(sum(nc1) != 0.0):
              av_nc = sum(nc1*en1*1000)/sum(nc1)
            else:
              av_nc = 0.0

            nomix_time.write(str(time[i-1])+"\t"+str(av_tot)+"\t"+str(av_ibd)+ \
                    "\t"+str(av_es)+"\t"+str(av_eo16)+"\t"+str(av_ao16)+"\t"+str(av_nc)+ \
                    "\t"+str(tot_tot)+"\t"+str(tot_ibd)+"\t"+str(tot_es)+"\t"+str(tot_eo16)+ \
                    "\t"+str(tot_ao16)+"\t"+str(tot_nc)+"\n")

        nomix_time.close()
        nomix_avg_tot = sum(nomix_total*nomix_en*1000)/sum(nomix_total)
        nomix_avg_ibd = sum(nomix_ibd*nomix_en*1000)/sum(nomix_ibd)
        nomix_avg_es = sum(nomix_es*nomix_en*1000)/sum(nomix_es)
        nomix_avg_eo16 = sum(nomix_eo16*nomix_en*1000)/sum(nomix_eo16)
        nomix_avg_ao16 = sum(nomix_ao16*nomix_en*1000)/sum(nomix_ao16)
        nomix_avg_nc = sum(nomix_nc*nomix_en*1000)/sum(nomix_nc)
        nomix_tot.write(str(m)+"\t"+str(nomix_avg_tot)+"\t"+str(nomix_avg_ibd)+"\t"+str(nomix_avg_es)+"\t"+str(nomix_avg_eo16)+"\t"+str(nomix_avg_ao16)+"\t"+str(nomix_avg_nc)+"\n")
