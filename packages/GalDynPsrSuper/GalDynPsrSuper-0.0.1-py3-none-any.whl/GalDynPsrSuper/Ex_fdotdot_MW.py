import math
import numpy as np
from . import read_parameters as par
from galpy.potential import MWPotential2014
from galpy.potential import KeplerPotential
from galpy.potential import evaluatezforces, evaluateRforces, evaluatePotentials
from galpy.potential import evaluatez2derivs,evaluateR2derivs,evaluateRzderivs
from galpy.util import conversion
from astropy import units as u
from . import ExGal_fdot_MW
from . import ExShk_fdot



def fdotdotexMW(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad):
         


    Rskpc = par.Rskpc
    Vs = par.Vs
    yrts = par.yrts
    c= par.c
    kpctom = par.kpctom
    Rs = Rskpc*kpctom
    mastorad = par.mastorad

    normpottoSI = par.normpottoSI
    normForcetoSI = par.normForcetoSI
    normjerktoSI = par.normjerktoSI


    b = bdeg*par.degtorad
    l = ldeg*par.degtorad

    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)

    zkpc = par.z(ldeg, bdeg, dkpc)

    fex_pl = ExGal_fdot_MW.Expl(ldeg, bdeg, dkpc)

    fex_z = ExGal_fdot_MW.Exz(ldeg, bdeg, dkpc)

    fex_shk = ExShk_fdot.Exshk(dkpc, mul, mub)
    
    fex_tot = fex_pl + fex_z + fex_shk


    #mub = mu_alpha #mas/yr
    #mul = mu_delta

    muT = (mub**2. + mul**2.)**0.5  
    #MWPotential2014= [MWPotential2014,KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc))] 
    #MWPot = [MWPotential2014,KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc))]  
    MWPot= MWPotential2014+KeplerPotential(amp=4*10**6./conversion.mass_in_msol(par.Vs,par.Rskpc)) 

    appl = -evaluateRforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI
    aspl = -evaluateRforces(MWPot, Rskpc/Rskpc,0.0/Rskpc)*normForcetoSI
    apz = evaluatezforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI



    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)
    coslpluslam = math.cos(l)*coslam - (Rskpc*math.sin(l)/Rpkpc)*math.sin(l)

    aTl1 = -(appl*(Rskpc*math.sin(l)/Rpkpc)-aspl*math.sin(l))
    aTb1 = appl*coslam*math.sin(b)+apz*math.cos(b) + aspl*math.cos(l)*math.sin(b)
    aTnet1 = (aTl1**2. + aTb1**2.)**(0.5)
    alphaV1 = math.atan2(mub,mul)/par.degtorad
    alphaA1 = math.atan2(aTb1,aTl1)/par.degtorad
    if alphaV1 < 0.:
       alphaV = 360.+alphaV1
    else:
       alphaV = alphaV1

    if alphaA1 < 0.:
       alphaA = 360.+alphaA1
    else:
       alphaA = alphaA1
    alpha = abs(alphaA - alphaV)



    aT1 = 2.*appl*aspl*coslpluslam
    aT2 = (c*(fex_pl+fex_z))**2.
    aTsq = appl**2. + aspl**2. + aT1 + apz**2. - aT2
    #if aTsq < 0.0:
    aT =  (appl**2. + aspl**2. + aT1 + apz**2. - aT2)**0.5



     
 
    zdot = (1000.0*vrad)*math.sin(b)+(mastorad/yrts)*mub*(dkpc*kpctom)*math.cos(b) 
    Rpdot = (1./(Rpkpc*kpctom))*(((dkpc*kpctom)*(math.cos(b)**2.) - Rs*math.cos(b)*math.cos(l))*(1000.0*vrad) + (Rs*(dkpc*kpctom)*math.sin(b)*math.cos(l) - ((dkpc*kpctom)**2.)*math.cos(b)*math.sin(b))*((mastorad/yrts)*mub) + Rs*(dkpc*kpctom)*math.sin(l)*((mastorad/yrts)*mul))
    #phiR2a = evaluateR2derivs(MWPot,Rpkpc/Rskpc,zkpc/Rskpc)
    phiR2 = normjerktoSI*evaluateR2derivs(MWPot,Rpkpc/Rskpc,zkpc/Rskpc)
    phiz2 = normjerktoSI*evaluatez2derivs(MWPot,Rpkpc/Rskpc,zkpc/Rskpc)
    phiRz = normjerktoSI*evaluateRzderivs(MWPot,Rpkpc/Rskpc,zkpc/Rskpc)
    phiR2sun = normjerktoSI*evaluateR2derivs(MWPot,Rskpc/Rskpc,0.0/Rskpc) 
    phiRzsun = normjerktoSI*evaluateRzderivs(MWPot,Rskpc/Rskpc,0.0/Rskpc)
    aspldot = phiR2sun*Rpdot + phiRzsun*zdot
    appldot = phiR2*Rpdot + phiRz*zdot
    if b>0:
      apzdot = phiRz*Rpdot + phiz2*zdot
    else:
      apzdot = -(phiRz*Rpdot + phiz2*zdot)
    
    #if coslam != 0.0 and Rpkpc != 0.0 and math.cos(b) != 0.0:
    
    lamdot = (1./coslam)*((Rs*math.cos(l)*((mastorad/yrts)*mul))/((Rpkpc*kpctom)*math.cos(b)) - (Rs*math.sin(l)/((Rpkpc*kpctom)**2.))*Rpdot)  
    ardot1 = math.sin(b)*(appl*coslam + aspl*math.cos(l))*((mastorad/yrts)*mub)         
    ardot2 = math.cos(b)*(appldot*coslam + aspldot*math.cos(l))
    ardot3 = apzdot*math.sin(abs(b))
    ardot4 = appl*math.cos(b)*(Rskpc*math.sin(l)/Rpkpc)*lamdot
    ardot5 = aspl*math.sin(l)*((mastorad/yrts)*mul)
    ardot6 = abs(apz)*math.cos(b)*((mastorad/yrts)*mub)*(b/abs(b))
    ardot = ardot1 - ardot2 - ardot3 + ardot4 + ardot5 - ardot6
   
    jerkt = (1./c)*(ardot - aT*((mastorad/yrts)*muT)*math.cos(alpha))   
  

    res1 = 2.*(mastorad/yrts)*(mub*((math.sin(b)/c)*(appl*coslam + aspl*math.cos(l)) + (math.cos(b)/c)*apz) - mul*(math.sin(l)/c)*(appl*(Rskpc/Rpkpc)-aspl))

    res2 = 2.*fex_tot*(math.cos(b)*math.cos(l)*(aspl/c) + (mastorad/yrts)*mub*(1000.*Vs/c)*math.sin(b)*math.sin(l) - (mastorad/yrts)*mul*(1000.*Vs/c)*math.cos(l))

    ssbt= res1+res2



   
    tsbt = (1./c)*(aT*((mastorad/yrts)*muT)*math.cos(alpha) - 3.*(1000.0*vrad)*(((mastorad/yrts)*muT)**2.))


    fourthterm = 2.*fex_tot*(fdotobs/f)


    Combterm = jerkt + ssbt + tsbt 


    fddotfex = -Combterm + fourthterm


   

    return fddotfex;


