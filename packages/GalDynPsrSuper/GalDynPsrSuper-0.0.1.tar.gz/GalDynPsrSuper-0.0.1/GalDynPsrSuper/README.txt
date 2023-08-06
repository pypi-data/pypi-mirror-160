# GalDynPsrSuper Package

GalDynPsrSuper is a package for calculating dynamical contributions to the first and the second derivatives of the frequencies (as well as periods), both spin or orbital, of pulsars in the Galactic field. These dynamical terms depend on the proper motion, the acceleration and the jerk of the pulsars. The main source of the acceleration of the pulsar is the gravitational potential of the Galaxy. GalDynPsrSuper uses two galpy based models of this potential: 1) 'MWPotential2014wBH' and 2) 'McMillan17'  and has the option to use either one of them. 

Details on various dynamical effects and formalism to estimate those are available in Pathak and Bagchi (ApJ 868 (2018) 123; arXiv: 1712.06590, hereafter Pathak and Bagchi (2018)) as well as Pathak and Bagchi (New Astronomy 85 (2021) 101549; arXiv: 1909.13113, hereafter Pathak and Bagchi (2021)). Please cite both the papers if you use GalDynPsrSuper for your research.

This package can calculate the fractional contributions or the excess terms, e.g. \dot{f}/f|_{excess, Gal}, \dot{f}/f|_{excess, Shk} (Eqs. (14),(15) and (19) of Pathak and Bagchi (2018)) and \ddot{f}/f|_excess (Eq. (11) of Pathak and Bagchi (2021)), where f is either the orbital frequency or the spin frequency. Similarly, in the period domain, this package can calculate the excess terms like \dot{P}/P|_{excess, Gal}, \dot{P}/P|_{excess, Shk} and \ddot{P}/P|_excess. 

Using the measured values of the frequency (or period), the derivative of the frequency (or period), and the second derivative of the frequency (or period), one can use GalDynPsrSuper even to compute the "intrinsic" values of the frequency (or period) derivative, as well as, the frequency (or period) second derivative, provided no other extra contribution exists.

A brief outline of the usage of GalDynPsrSuper is given below.

# 1) Install GalDynPsrSuper as pip3 install GalDynPsrSuper (assuming you have numpy, scipy, and galpy already installed and working)

We have tested with galpy version 1.7.2 and suggest the users to upgrade galpy if they have older versions (much older versions did not have the McMillan potential and there might be additional discrepancies as well).
If wished, one can change the values of Rs (Galactocentric cylindrical radius of the Sun) and Vs (rotational speed of the Sun around the Galactic centre) in the parameters.in file that can be found inside the GalDynPsrSuper (installed directory).
But remember that galpy also has these values defined in the file '$home/.galpyrc'. One can in principle change the values in both of the files. However, the Milky Way potential in galpy was fitted with Rs = 8 kpc and Vs = 220 km/s in galpy.


# 2) Import GalDynPsrSuper

import GalDynPsrSuper


# 3)

A) Observable parameters needed to compute \dot{f}/f|_{excess, Gal}: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), and the proper motion in the Galactic latitude in mas/yr (say mub).

B) Observable parameters needed to compute \dot{P}/P|_{excess, Gal}: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), and the proper motion in the Galactic latitude in mas/yr (say mub).

C) Observable parameters needed to compute \dot{f}/f|_{excess, Shk}: the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), and the proper motion in the Galactic latitude in mas/yr (say mub).

D) Observable parameters needed to compute \dot{P}/P|_{excess, Shk}: the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), and the proper motion in the Galactic latitude in mas/yr (say mub).

E) Observable parameters needed to compute \ddot{f}/f|_excess: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), the proper motion in the Galactic latitude in mas/yr (say mub), the radial component of the relative velocity of the pulsar with respect to the solar system barycenter in km/s (say vrad), the frequency in Hz (say f), and the observed frequency derivative in s^{-2} (say fdotobs). 

F) Observable parameters needed to compute \ddot{P}/P|_excess: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), the proper motion in the Galactic latitude in mas/yr (say mub), the radial component of the relative velocity of the pulsar with respect to the solar system barycenter in km/s (say vrad), the period in s (say p), and the observed period derivative in s^{-2} (say pdotobs). 


The frequency and its derivatives can either be spin or orbital. Similarly, the period and its derivatives can either be spin or orbital.

# 4) Remember that the module names are case sensitive, so use them as demonstrated below. Also, for each case, ordering of the parameters must be as shown.

# 5) Calculate the Galactic contribution to the excess term for the first derivative of the frequency using the two Milky Way Potential models as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_fdot_MW.ExGalfdotMW(ldeg, bdeg, dkpc)

b) When using McMillan17:
GalDynPsrSuper.ExGal_fdot_MC.ExGalfdotMC(ldeg, bdeg, dkpc)

# 6) Calculate the Galactic contribution to the excess term for the first derivative of the period using the two Milky Way Potential models as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_pdot_MW.ExGalpdotMW(ldeg, bdeg, dkpc)

b) When using McMillan17:
GalDynPsrSuper.ExGal_pdot_MC.ExGalpdotMC(ldeg, bdeg, dkpc)


# 7) Calculate the Shklovskii term contribution to the excess term for the first derivative of the frequency as:

GalDynPsrSuper.ExShk_fdot.Exshk(dkpc, mul, mub) 

 This term is independent of the Galactic potential model.

# 8) Calculate the Shklovskii term contribution to the excess term for the first derivative of the period as:

GalDynPsrSuper.ExShk_pdot.Exshk(dkpc, mul, mub) 

 This term is independent of the Galactic potential model.


# 9) Calculate the total excess term in the first derivative of the frequency, say fdotex, as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_fdot_MW.ExGalfdotMW(ldeg, bdeg, dkpc) + GalDynPsrSuper.ExShk_fdot.Exshk(dkpc, mul, mub)

b) When using McMillan17:
GalDynPsrSuper.ExGal_fdot_MC.ExGalfdotMC(ldeg, bdeg, dkpc) + GalDynPsrSuper.ExShk_fdot.Exshk(dkpc, mul, mub)


# 10) Calculate the total excess term in the first derivative of the period, say pdotex, as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_pdot_MW.ExGalpdotMW(ldeg, bdeg, dkpc) + GalDynPsrSuper.ExShk_pdot.Exshk(dkpc, mul, mub) 

b) When using McMillan17:
GalDynPsrSuper.ExGal_pdot_MC.ExGalpdotMC(ldeg, bdeg, dkpc) + GalDynPsrSuper.ExShk_pdot.Exshk(dkpc, mul, mub)


One needs to assign the values of ldeg, bdeg, dkpc, mul, and mub before calling the above functions.



# 11) Print the basic parameters of the pulsars

GalDynPsrSuper.read_parameters.Rskpc returns the Galactocentric cylindrical radius of the Sun (Rs in kpc or Rskpc).

GalDynPsrSuper.read_parameters.Vs returns the rotational speed of the Sun around the Galactic centre (Vs in km/s).

GalDynPsrSuper.read_parameters.Rpkpc(ldeg, bdeg, dkpc) returns the value of Galactocentric cylindrical radius of the pulsar in kpc (Rp in kpc or Rpkpc).

GalDynPsrSuper.read_parameters.z(ldeg, bdeg, dkpc) returns the perpendicular distance of the pulsar from the Galactic plane (z in kpc or zkpc). 

The meaning of the arguments in the above examples are as usual.


# 12) Calculate the intrinsic frequency derivative, say fdotint, as: 

User needs observed value of the frequency derivative, say fdotobs in seconds^(-2). Using the total excess term fdotex from point 9) and frequency, say f in Hz, we can get fdotint in seconds^(-2) as

fdotint = fdotobs - fdotex * f   

# 13) Calculate the intrinsic period derivative , say pdotint, as:

User needs observed value of the period derivative, say pdotobs in seconds*seconds^(-1). Using the total excess term pdotex from point 10) and period, say p in seconds, we can get pdotint in seconds*seconds^(-1) as

pdotint = pdotobs - pdotex * p



# 14) Calculate the excess terms in the second derivative of the frequency, say fdotdotex, using the two Milky Way Potential models as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_fdotdot_MW.fdotdotexMW(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad)

b) When using McMillan17:
GalDynPsrSuper.ExGal_fdotdot_MC.fdotdotexMC(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad)

Here, for both the cases, in addition to assigning the values of ldeg, bdeg, dkpc, mul, mub, f, and fdotobs, one needs to also assign the measured value of the radial component of the relative velocity of the pulsar, 'vrad', in km/s.

# 15) Calculate the excess terms in the second derivative of the period, say pdotdotex, using the two Milky Way Potential models as shown below,

a) When using MWPotential2014wBH:
GalDynPsrSuper.ExGal_pdotdot_MW.pdotdotexMW(ldeg, bdeg, dkpc, mul, mub, p, pdotobs, vrad)

b) When using McMillan17:
GalDynPsrSuper.ExGal_pdotdot_MC.pdotdotexMC(ldeg, sbdeg, dkpc, mul, mub, p, pdotobs, vrad)

Here, for both the cases, in addition to assigning the values of ldeg, bdeg, dkpc, mul, mub, p, and pdotobs, one needs to also assign the measured value of the radial component of the relative velocity of the pulsar, 'vrad', in km/s.



# 16) Calculate the intrinsic value of second derivative of frequency, say fdotdotint, as: 

User needs observed value of the second derivative of frequency, say fdotdotobs in seconds^(-3). Using the total excess term fdotdotex from point 14) and frequency, say f in Hz, we can get fdotint in seconds^(-3)as

fdotdotint = fdotdotobs - fdotdotex * f   


# 17) Calculate the intrinsic value of second derivative of period, say pdotdotint, as: 

User needs observed value of the period derivative, say pdotdotobs in seconds*seconds^(-2). Using the total excess term pdotdotex from point 15) and period, say p in seconds, we can get pdotint in seconds*seconds^(-2) as

pdotdotint = pdotdotobs - pdotdotex * p



### #####Example#####

### Using model MWPotential2014wBH  

import GalDynPsrSuper

ldeg = 20.0

bdeg= 20.0

dkpc = 2.0

mul = 20.0

mub = 20.0

vrad = 20.0

f = 50.0

fdotobs = -1.43e-15

fdotdotobs = 1.2e-28

Rpkpc = GalDynPsrSuper.read_parameters.Rpkpc(ldeg, bdeg, dkpc) 

Output: 6.267007084433072


zkpc = GalDynPsrSuper.read_parameters.z(ldeg, bdeg, dkpc) 

Output: 0.6840402866513374


fex_Gal = GalDynPsrSuper.ExGal_fdot_MW.ExGalfdotMW(ldeg, bdeg, dkpc) 

Output: -3.836151248676907e-21


fex_shk = GalDynPsrSuper.ExShk_fdot.Exshk(dkpc, mul, mub) 

Output: -3.886794901984e-18
 

fdotex = fex_Gal + fex_shk

Output: -3.890631053232677e-18


fdotint = fdotobs - fdotex * f  

Output: -1.2354684473383662e-15


fdotdotfex = GalDynPsrSuper.Ex_fdotdot_MW.fdotdotexMW(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad) 

Output: 9.32211733880072e-33


fddotint = fdotdotobs - fdotdotfex * f 

Output: 1.1953389413305997e-28




#========================================================================================
### #####Contents of the Package#####

Files:

parameters.in: Input file, that contains values of constants which are subject to change with improvements in measurements. User can change the values of the constants if the need be. These constants are Vs (rotational speed of the Sun around the Galactic centre in km/s) and Rskpc (Galactocentric radius of the Sun, Rs, in kpc). Rs is defined in a cylindrical coordinate system. 

README.txt: Contents of this README.md file inside package along with code files.

Description of different codes:

read_parameters.py: Contains various constants used in the package, as well as, functions to calculate Rp(kpc) and z(kpc).

ExGal_pdot_MW.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess term \dot{P}/P|_excess using 'MWPotential2014wBH' as the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

ExGal_pdot_MC.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess term \dot{P}/P|_excess using 'McMillan17' as the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

ExGal_fdot_MW.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess term \dot{f}/f|_excess using 'MWPotential2014wBH' as the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

ExGal_fdot_MC.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess term \dot{P}/P|_excess using 'McMillan17' as the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

ExShk_pdot.py: Calculates the Shklovskii term contibution to \dot{P}/P|_excess, i.e., d(mu_T*mu_T)/c, where d is the distance of the pulsar from the solar system barycentre, mu_T is the total proper motion of the pulsar, and c is the speed of light. The required arguments for this module are the observables dkpc, mul, and mub.

ExShk_fdot.py: Calculates the Shklovskii term contibution to \dot{f}/f|_excess, i.e., -d(mu_T*mu_T)/c, where d is the distance of the pulsar from the solar system barycentre, mu_T is the total proper motion of the pulsar, and c is the speed of light. The required arguments for this module are the observables dkpc, mul, and mub.

Ex_pdotdot_MW.py: Calculates the total excess term for the second derivative of the period \ddot{P}/P|_excess using the effect of 'MWPotential2014wBH' as the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, p, pdotobs, and vrad.

Ex_pdotdot_MC.py: Calculates the total excess term for the second derivative of the period \ddot{P}/P|_excess using the effect of 'McMillan17' as the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, p, pdotobs, and vrad.

Ex_fdotdot_MW.py: Calculates the total excess term for the second derivative of the frequency \ddot{f}/f|_excess using the effect of 'MWPotential2014wBH' as the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, fdotobs, and vrad.

Ex_fdotdot_MC.py: Calculates the total excess term for the second derivative of the frequency \ddot{f}/f|_excess using the effect of 'McMillan17' as the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, fdotobs, and vrad.

############################################################


