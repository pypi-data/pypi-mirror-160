import math
from galpy.potential import MWPotential2014
from galpy.potential import PowerSphericalPotentialwCutoff
from galpy.potential import MiyamotoNagaiPotential
from galpy.potential import NFWPotential
from galpy.util import conversion
from astropy import units
from galpy.potential import KeplerPotential
from galpy.potential import evaluateRforces
from galpy.potential import evaluatezforces
from . import read_parameters as par



def MWBHRfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)


    #MWPotential2014BH= [MWPotential2014,KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc))]
    MWPotential2014BH= MWPotential2014+KeplerPotential(amp=4*10**6./conversion.mass_in_msol(Vs,Rskpc))


    rforce1 = evaluateRforces(MWPotential2014BH, Rpkpc/Rskpc,zkpc/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss

    rfsun = evaluateRforces(MWPotential2014BH, Rskpc/Rskpc,0.0/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    
    rf0 = rforce1*coslam + rfsun*math.cos(l) #m/ss
    rf = rf0*math.cos(b)/par.c # s-1
    return rf;


def MWBHZfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
  
    #MWPotential2014BH= [MWPotential2014,KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc))]
    MWPotential2014BH= MWPotential2014+KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc))

    zf1 = evaluatezforces(MWPotential2014BH, Rpkpc/Rskpc,zkpc/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    Excz = zf1*math.sin(b)/par.c #s-1
    return Excz;



def Expl(ldeg, bdeg, dkpc):
   excpl = -MWBHRfo(ldeg, bdeg, dkpc) #s^-1 
   return excpl;

def Exz(ldeg, bdeg, dkpc):
   exz = -MWBHZfo(ldeg, bdeg, dkpc) #s^-1 
   return exz;

def ExGalfdotMW(ldeg, bdeg, dkpc):
   return -MWBHRfo(ldeg, bdeg, dkpc) - MWBHZfo(ldeg, bdeg, dkpc);    


