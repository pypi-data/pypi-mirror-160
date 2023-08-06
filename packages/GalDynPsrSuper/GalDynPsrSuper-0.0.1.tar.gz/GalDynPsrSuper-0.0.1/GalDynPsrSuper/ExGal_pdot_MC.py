import math
from galpy.potential.mwpotentials import McMillan17
from galpy.util import conversion
from galpy.potential import evaluateRforces
from galpy.potential import evaluatezforces
from astropy import units
from . import read_parameters as par




def McMillanRfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)


    rforce1 = evaluateRforces(McMillan17, Rpkpc/Rskpc,zkpc/Rskpc,use_physical=False)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss

    rfsun = evaluateRforces(McMillan17, Rskpc/Rskpc,0.0/Rskpc,use_physical=False)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss


    rf0 = rforce1*coslam + rfsun*math.cos(l) #m/ss
    rf = rf0*math.cos(b)/par.c # s-1
    return rf;



def McMillanZfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
  

    zf1 = evaluatezforces(McMillan17, Rpkpc/Rskpc,zkpc/Rskpc,use_physical=False)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    Excz = zf1*math.sin(b)/par.c #s-1
    return Excz;



def Expl(ldeg, bdeg, dkpc):
   excpl = McMillanRfo(ldeg, bdeg, dkpc) #s^-1 
   return excpl;

def Exz(ldeg, bdeg, dkpc):
   exz = McMillanZfo(ldeg, bdeg, dkpc) #s^-1 
   return exz;


def ExGalpdotMC(ldeg, bdeg, dkpc):
   return Expl(ldeg, bdeg, dkpc) + Exz(ldeg, bdeg, dkpc);    


