import os


def run(a,m,timebins,material,detector):
    """Runs snowglobes on generated 'pinched' files \n
    Input: alpha value, mass value, \n
        timebins: time bins of snowglobes data \n
        detector material and detector configuration \n
    Output: None"""

    for n in range(len(timebins)):
        os.system("./supernova.pl pinched_a"+str(a)+"_m"+str(m)+"_"+str(n+1) \
                +" "+str(material)+" "+str(detector))
