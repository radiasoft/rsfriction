# from __future__ import division

#-------------------------------------
#
#        Started at 07/25/2017 (YuE)
# 
#-------------------------------------

import os, sys
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import matplotlib as mpl

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import scipy.integrate as integrate
from scipy.integrate import quad, nquad, dblquad

from scipy.constants import pi
from scipy.constants import speed_of_light as clight
from scipy.constants import epsilon_0 as eps0
from scipy.constants import mu_0 as mu0
from scipy.constants import elementary_charge as qe
from scipy.constants import electron_mass as me
from scipy.constants import proton_mass as mp
from scipy.constants import Boltzmann as kB


eVtoErg=1.602e-12                # energy from eV to erg (from CI to CGS)
#
# Initial parameters:
#
Z_ion = qe*2.997e+9              # charge of ion (proton), CGSE units of the charge
M_ion = mp*1.e+3                 # mass of ion (proton), g
q_elec = qe*2.997e+9             # charge of electron, CGSE units of the charge
m_elec = me*1.e+3                # mass of electron, g
tangAlpha=1.                     # to calculate length of interaraction
B_mag = 2000.                    # magnetic field, Gs
Temp_eTran = 0.5                 # transversal temperature of electrons, eV
Temp_eLong = 2.e-4               # longitudinal temperature of electrons, eV
numb_e = 1000                    # number of electrons
numb_p = 50                      # number of protons

a_eBeam = 0.1                    # cm
n_eBeam = 1.e+9                  # cm^-3

stepsNumberOnGyro = 40           # number of the steps on each Larmour period

#
# Larmor frequency electron:
#
def omega_Larmor(mass,B_mag):
    return (q_elec)*B_mag/(mass*clight*1.e+2)             # rad/sec

#
# Derived quantities:
#
#
# The longitudinal shift velocities of the electrons and ions are the same:
# 
tempRatio=Temp_eLong/Temp_eTran                           # dimensionless
velRatio=np.sqrt(tempRatio)                               # dimensionless
print 'tempRatio = %e, velRatio = %e' % (tempRatio,velRatio)


omega_L = omega_Larmor(m_elec, B_mag)                     # rad/sec 
T_larm = 2*pi/omega_L                                     # sec
timeStep = T_larm/stepsNumberOnGyro                       # time step, sec
print 'omega_Larmor= %e rad/sec, T_larm = %e sec, timeStep = %e sec' % (omega_L,T_larm,timeStep)

rmsV_eTran = np.sqrt(2.*Temp_eTran*eVtoErg/m_elec)        # cm/sec
rmsV_eLong = np.sqrt(2.*Temp_eLong*eVtoErg/m_elec)        # cm/sec
print 'rmsV_eTran = %e cm/sec, rmsV_eLong = %e cm/sec' % (rmsV_eTran,rmsV_eLong)

ro_larm = rmsV_eTran/omega_L                              # cm
print '<ro_larm> = %e cm' % ro_larm

omega_e=np.sqrt(4*pi*n_eBeam*q_elec**2/m_elec)            # rad/sec
print 'omega_e = %e rad/sec' % omega_e

#
# Electrons are magnetized for impact parameter >> rhoCrit:
#
rhoCrit=math.pow(q_elec**2/(m_elec*omega_L**2),1./3)      # cm
maxLogRho=math.log10(a_eBeam/rhoCrit)
minLogRho=-1.

print 'rhoCrit = %e cm, maxLogRho = %e' % (rhoCrit,maxLogRho)


pointsRo=50
minB=.1                    # Gs
maxB=4000.                 # Gs

crrntB=np.zeros(pointsRo)
roCrtCrrnt=np.zeros(pointsRo)

for i in range(pointsRo):
   crrntB[i]=minB+(maxB-minB)/pointsRo*(i+1)
   freqL=q_elec*crrntB[i]/(m_elec*clight*1.e+2)
   roCrtCrrnt[i]=math.pow(q_elec**2/m_elec/freqL**2,1./3.)
   
fig5=plt.figure(5)
plt.plot(crrntB,1e+4*roCrtCrrnt,'-r',linewidth=2)   
plt.xlabel('B, Gs',color='m',fontsize=16)
plt.ylabel('$ro_{crit}$, $\mu$m',color='m',fontsize=16)
plt.title('Area of of Magnetization: $ro$ >> $ro_{crit}=[Z_ie^2/(m\cdot\omega_L^2)]^{1/3}$',color='m',fontsize=16)
# plt.xlim([minLogRho,maxLogRho])
plt.grid(True)
   
   
   
pointsLog10=50
log10Rho=np.zeros(pointsLog10)
rhoCrrnt=np.zeros(pointsLog10)
omega_z=np.zeros(pointsLog10)
Omega=np.zeros(pointsLog10)
omega_p=np.zeros(pointsLog10)
omega_m=np.zeros(pointsLog10)
relOmegas=np.zeros(pointsLog10)
for i in range(pointsLog10):
   log10Rho[i]=minLogRho+(maxLogRho-minLogRho)/(pointsLog10-1)*i
   rhoCrrnt[i]=rhoCrit*math.pow(10.,log10Rho[i])
   omega_z[i]=np.sqrt(q_elec**2/(m_elec*rhoCrrnt[i]**3))
   Omega[i]=np.sqrt(omega_L**2+4.*omega_z[i]**2)
   relOmegas[i]=omega_z[i]/Omega[i]
   omega_p[i]=.5*(omega_L+Omega[i])
   omega_m[i]=.5*(omega_L-Omega[i])

# print 'rhoCrrnt =', rhoCrrnt

'''
fig10=plt.figure(10)
plt.semilogy(range(pointsLog10),rhoCrrnt/rhoCrit,'.r')   
plt.xlabel('Point',color=','m',fontsize=16)
plt.ylabel('$ro/ro_{crit}$',color='m',fontsize=16)
plt.title('$ro/ro_{crit}$',color='m',fontsize=16)
# plt.xlim([minLogRho,maxLogRho])
plt.grid(True)
'''   
   
'''   
fig20=plt.figure(20)
plt.loglog(rhoCrrnt/rhoCrit,omega_z,'.r')   
plt.xlim([rhoCrrnt[0]/rhoCrit,rhoCrrnt[pointsLog10-1]/rhoCrit])
plt.xlabel('$ro/ro_{crit}$',color='m',fontsize=16)
plt.ylabel('$\omega_z$, sec',color='m',fontsize=16)
plt.title('$\omega_z$',color='m',fontsize=16)
plt.grid(True)
'''
   
fig30=plt.figure(30)
plt.loglog(rhoCrrnt/rhoCrit,omega_z/omega_L,'-r',linewidth=2)   
plt.hold(True)  
plt.plot([1.,1.],[1.e-5,1.e2],'--m',linewidth=2)
plt.xlim([rhoCrrnt[0]/rhoCrit,rhoCrrnt[pointsLog10-1]/rhoCrit])
# plt.xlabel('Impact Parameter: $ro/ro_{crit}$; $ro_{crit}=[Z_ie^2/(m\cdot\omega_L^2)]^{1/3}$',color='m',fontsize=16)
plt.xlabel('Impact Parameter: $ro/ro_{crit}$',color='m',fontsize=16)
plt.ylabel('$\omega_z/\omega_L$',color='m',fontsize=16)
plt.title('$\omega_z/\omega_L=(ro/ro_{crit})^{-3/2}$',color='m',fontsize=16)
plt.grid(True)
plt.text(2.,10.,'"Magnetization" Area',color='m',fontsize=25)
plt.text(2.8,1.,'$ro_{crit}=[Z_ie^2/(m\cdot\omega_L^2)]^{1/3}$',color='m',fontsize=20)
   
'''   
fig40=plt.figure(40)
plt.semilogx(rhoCrrnt/rhoCrit,Omega,'.r')   
plt.xlim([rhoCrrnt[0]/rhoCrit,rhoCrrnt[pointsLog10-1]/rhoCrit])
plt.xlabel('$ro/ro_{crit}$',color='m',fontsize=16)
plt.ylabel('$\Omega$, sec',color='m',fontsize=16)
plt.grid(True)
'''
   
fig50=plt.figure(50)
plt.semilogx(rhoCrrnt/rhoCrit,Omega/omega_L,'-r',linewidth=2)   
plt.xlim([rhoCrrnt[0]/rhoCrit,rhoCrrnt[pointsLog10-1]/rhoCrit])
plt.xlabel('Impact Parameter: $ro/ro_{crit}$; $ro_{crit}=[Z_ie^2/(m\cdot\omega_L^2)]^{1/3}$',color='m',fontsize=16)
plt.ylabel('$\Omega/\omega_L$',color='m',fontsize=16)
plt.title('$\Omega=[\omega_L^2+4\cdot\omega_z^2]^{1/2}=\omega_L\cdot[1+4/(ro/ro_{crit})^3]^{1/2}$', \
          color='m',fontsize=16)
plt.grid(True)

fig55=plt.figure(55)
plt.semilogx(rhoCrrnt/rhoCrit,Omega/omega_L,'-r',linewidth=2)   
plt.xlim([1.,rhoCrrnt[pointsLog10-1]/rhoCrit])
plt.ylim([0.9,2.5])
plt.xlabel('Impact Parameter: $ro/ro_{crit}$; $ro_{crit}=[Z_ie^2/(m\cdot\omega_L^2)]^{1/3}$',color='m',fontsize=16)
plt.ylabel('$\Omega/\omega_L$',color='m',fontsize=16)
plt.title('$\Omega=[\omega_L^2+4\cdot\omega_z^2]^{1/2}=\omega_L\cdot[1+4/(ro/ro_{crit})^3]^{1/2}$', \
          color='m',fontsize=16)
plt.grid(True)

'''   
fig60=plt.figure(60)
plt.loglog(rhoCrrnt/rhoCrit,relOmegas,'-r')   
plt.xlim([rhoCrrnt[0]/rhoCrit,rhoCrrnt[pointsLog10-1]/rhoCrit])
plt.xlabel('$ro/ro_{crit}$',color='m',fontsize=16)
plt.ylabel('$\omega_z/\Omega$',color='m',fontsize=16)
plt.title('$\omega_z/\Omega$',color='m',fontsize=16)
plt.grid(True)
'''
   
   
N_ppt=80
turns=10
pointsPhi=N_ppt*turns
fi=np.zeros(pointsPhi)

Omega_omega_L=[np.sqrt(5.),1./0.577,1.2,1.00001]


ro=np.zeros(4)
ampl=np.zeros(4)
delta_r=np.zeros(4)
omega_p_omega_L=np.zeros(4)
omega_m_omega_L=np.zeros(4)
omega_z_omega_L=np.zeros(4)
omega_z_Omega=np.zeros(4)
widthTorus=np.zeros(4)
ro_roCrit=np.zeros(4)

r=np.zeros((pointsPhi,4))              # dimensionless in unit ro_L
x=np.zeros((pointsPhi,4))              # dimensionless in unit ro_L
y=np.zeros((pointsPhi,4))              # dimensionless in unit ro_L

for j in range(4):
   ro[j]=math.pow(Z_ion*q_elec**2/m_elec/omega_L**2/(Omega_omega_L[j]**2-1),1./3.)
   omega_p_omega_L[j]=.5*(1+Omega_omega_L[j])
   omega_m_omega_L[j]=.5*(1-Omega_omega_L[j])
   ampl[j]=1.-1./Omega_omega_L[j]**2
   delta_r[j]=1.-np.sqrt(1.-ampl[j])
   omega_z_omega_L[j]=.5*np.sqrt(Omega_omega_L[j]**2-1.)
   omega_z_Omega[j]=omega_z_omega_L[j]/Omega_omega_L[j]
   widthTorus[j]=1.-np.sqrt(1-4.*omega_z_Omega[j]**2)
   ro_roCrit[j]=(1./(omega_z_Omega[j]*Omega_omega_L[j]))**(2./3.)
   print 'Omega_omega_L[%d]=%e, delta_r=%e, omega_z_omega_L=%e, omega_z_Omega=%e, width=%e, ro_roCrit=%e' % \
         (j,Omega_omega_L[j],delta_r[j],omega_z_omega_L[j],omega_z_Omega[j],widthTorus[j],ro_roCrit[j])

print 'ro, ro/ro_c: ',  (ro, ro/rhoCrit)

stepT=2*pi/omega_L

# print ' stepT = %e, Omega_omegaL=%e:, omega_p_omega_L=%e, omega_m_omega_L=%e' % \
#       (stepT, Omega_omega_L,omega_p_omega_L,omega_m_omega_L)

#
# This parameter means, that electron does not come near the ion
# by a distance less then rhoCrit 
#
# shift_ro=1.+rhoCrit/ro_larm
#
# In case under consideration ro_larm/rhoCrit equals approx 20.
# Therefore shift_ro is practically 1:
shift_ro=1.

for i in range(N_ppt*turns):
   fi[i]=2*pi/N_ppt*i
# print 'fi[0:41]= ', fi[0:41]

for j in range(4):
   pnt=0
   for turn in range(turns):
      for i in range(N_ppt):
         x[pnt,j]=(shift_ro*omega_p_omega_L[j]*math.cos(omega_m_omega_L[j]*fi[pnt])- \
                 shift_ro*omega_m_omega_L[j]*math.cos(omega_p_omega_L[j]*fi[pnt])+ \
	         math.cos(omega_p_omega_L[j]*fi[pnt])-math.cos(omega_m_omega_L[j]*fi[pnt]))/Omega_omega_L[j]
         y[pnt,j]=(shift_ro*omega_p_omega_L[j]*math.sin(omega_m_omega_L[j]*fi[pnt])+ \
                 shift_ro*omega_m_omega_L[j]*math.sin(omega_p_omega_L[j]*fi[pnt])+ \
	         math.sin(omega_p_omega_L[j]*fi[pnt])-math.sin(omega_m_omega_L[j]*fi[pnt]))/Omega_omega_L[j]
         r[pnt,j]=np.sqrt(1-ampl[j]*math.sin(.5*Omega_omega_L[j]*fi[pnt])**2)
         pnt += 1
   
fig70=plt.figure(70)
# plt.plot(fi[0:1.5*N_ppt],r[0:1.5*N_ppt,0],'-r',fi[0:1.5*N_ppt],r[0:1.5*N_ppt,1],'-b', \
#          fi[0:1.5*N_ppt],r[0:1.5*N_ppt,2],'-m',fi[0:1.5*N_ppt],r[0:1.5*N_ppt,3],'-g',linewidth=2) 
plt.plot(fi[0:1.5*N_ppt],r[0:1.5*N_ppt,0],'-r',fi[0:1.5*N_ppt],r[0:1.5*N_ppt,1],'-b', \
         fi[0:1.5*N_ppt],r[0:1.5*N_ppt,2],'-m',linewidth=2) 
plt.xlabel('$\phi=\omega_L\cdot t$',color='m',fontsize=16)
plt.ylabel('$r(t)/ro_L$',color='m',fontsize=16)
plt .ylim([0.,1.])
plt.title('$r(t)/ro_L=[1-4\omega_z^2/\Omega^2\cdot sin^2(\Omega t/2)]^{1/2}$,  $\Omega=[\omega_L^2+4\cdot\omega_z^2]^{1/2}$',color='m',fontsize=16)
plt.legend(['$\Omega/\omega_L=2.236$','$\Omega/\omega_L=1.733$','$\Omega/\omega_L=1.200$'],fontsize=16,loc='lower right')
plt.grid(True)

fig75=plt.figure(75)
plt.plot(fi[0:1.5*N_ppt],(1-r[0:1.5*N_ppt,3])*1e+4,'-r',linewidth=2) 
# plt.plot(fi[0:1.5*N_ppt],r[0:1.5*N_ppt,3],'-r',linewidth=2) 
plt.xlabel('$\phi=\omega_L\cdot t$',color='m',fontsize=16)
plt.ylabel('$10^5\cdot[1-r(t)/ro_L]$',color='m',fontsize=16)
plt.title('$r(t)/ro_L=[1-4\omega_z^2/\Omega^2\cdot sin^2(\Omega t/2)]^{1/2}$,  $\Omega=[\omega_L^2+4\cdot\omega_z^2]^{1/2}$',color='m',fontsize=16)
plt.legend(['$\Omega/\omega_L=1.00001$'],fontsize=16,loc='upper right')
plt.grid(True)
# plt.ylim([.99998,1.])

fig80=plt.figure(80)
plt.plot(x[0*N_ppt:1*N_ppt+1,0],y[0*N_ppt:1*N_ppt+1,0],'-r',linewidth=2) 
plt.hold(True)  
plt.plot(x[1*N_ppt:2*N_ppt+1,0],y[1*N_ppt:2*N_ppt+1,0],'-b',linewidth=2) 
plt.plot(x[2*N_ppt:3*N_ppt+1,0],y[2*N_ppt:3*N_ppt+1,0],'-m',linewidth=2) 
plt.plot(x[3*N_ppt:4*N_ppt+1,0],y[3*N_ppt:4*N_ppt+1,0],'-g',linewidth=2) 
plt.plot(x[4*N_ppt:5*N_ppt+1,0],y[4*N_ppt:5*N_ppt+1,0],'-k',linewidth=2) 
plt.plot(x[5*N_ppt:6*N_ppt+1,0],y[5*N_ppt:6*N_ppt+1,0],'-xr',linewidth=2,markersize=10) 
plt.plot(x[6*N_ppt:7*N_ppt+1,0],y[6*N_ppt:7*N_ppt+1,0],'-xb',linewidth=2,markersize=10) 
plt.plot(x[7*N_ppt:8*N_ppt+1,0],y[7*N_ppt:8*N_ppt+1,0],'-xm',linewidth=2,markersize=10) 
plt.plot(x[8*N_ppt:9*N_ppt+1,0],y[8*N_ppt:9*N_ppt+1,0],'-xg',linewidth=2,markersize=10) 
plt.xlabel('$x/ro_L$',color='m',fontsize=16)
plt.ylabel('$y/ro_L$',color='m',fontsize=16)
titleHeader='First 9 Turns: $\Omega/\omega_L=$%5.3f, $ro/ro_{crit}=$%5.3f'
plt.title(titleHeader % (Omega_omega_L[0],ro_roCrit[0]),color='m',fontsize=16)
plt.grid(True)
plt.axes().set_aspect('equal')

   
fig90=plt.figure(90)
plt.plot(x[0*N_ppt:1*N_ppt+1,1],y[0*N_ppt:1*N_ppt+1,1],'-r',linewidth=2) 
plt.hold(True)  
plt.plot(x[1*N_ppt:2*N_ppt+1,1],y[1*N_ppt:2*N_ppt+1,1],'-b',linewidth=2) 
plt.plot(x[2*N_ppt:3*N_ppt+1,1],y[2*N_ppt:3*N_ppt+1,1],'-m',linewidth=2) 
plt.plot(x[3*N_ppt:4*N_ppt+1,1],y[3*N_ppt:4*N_ppt+1,1],'-g',linewidth=2) 
plt.plot(x[4*N_ppt:5*N_ppt+1,1],y[4*N_ppt:5*N_ppt+1,1],'-k',linewidth=2) 
plt.plot(x[5*N_ppt:6*N_ppt+1,1],y[5*N_ppt:6*N_ppt+1,1],'-xr',linewidth=2,markersize=10) 
plt.plot(x[6*N_ppt:7*N_ppt+1,1],y[6*N_ppt:7*N_ppt+1,1],'-xb',linewidth=2,markersize=10) 
plt.plot(x[7*N_ppt:8*N_ppt+1,1],y[7*N_ppt:8*N_ppt+1,1],'-xm',linewidth=2,markersize=10) 
plt.plot(x[8*N_ppt:9*N_ppt+1,1],y[8*N_ppt:9*N_ppt+1,1],'-xg',linewidth=2,markersize=10) 
plt.xlabel('$x/ro_L$',color='m',fontsize=16)
plt.ylabel('$y/ro_L$',color='m',fontsize=16)
titleHeader='First 9 Turns: $\Omega/\omega_L=$%5.3f, $ro/ro_{crit}=$%5.3f'
plt.title(titleHeader % (Omega_omega_L[1],ro_roCrit[1]),color='m',fontsize=16)
plt.grid(True)
plt.axes().set_aspect('equal')
 
     
fig100=plt.figure(100)
plt.plot(x[0*N_ppt:1*N_ppt+1,2],y[0*N_ppt:1*N_ppt+1,2],'-r',linewidth=2) 
plt.hold(True)  
plt.plot(x[1*N_ppt:2*N_ppt+1,2],y[1*N_ppt:2*N_ppt+1,2],'-b',linewidth=2) 
plt.plot(x[2*N_ppt:3*N_ppt+1,2],y[2*N_ppt:3*N_ppt+1,2],'-m',linewidth=2) 
plt.plot(x[3*N_ppt:4*N_ppt+1,2],y[3*N_ppt:4*N_ppt+1,2],'-g',linewidth=2) 
plt.plot(x[4*N_ppt:5*N_ppt+1,2],y[4*N_ppt:5*N_ppt+1,2],'-k',linewidth=2) 
plt.plot(x[5*N_ppt:6*N_ppt+1,2],y[5*N_ppt:6*N_ppt+1,2],'-xr',linewidth=2,markersize=10) 
plt.plot(x[6*N_ppt:7*N_ppt+1,2],y[6*N_ppt:7*N_ppt+1,2],'-xb',linewidth=2,markersize=10) 
plt.plot(x[7*N_ppt:8*N_ppt+1,2],y[7*N_ppt:8*N_ppt+1,2],'-xm',linewidth=2,markersize=10) 
plt.plot(x[8*N_ppt:9*N_ppt+1,2],y[8*N_ppt:9*N_ppt+1,2],'-xg',linewidth=2,markersize=10) 
plt.xlabel('$x/ro_L$',color='m',fontsize=16)
plt.ylabel('$y/ro_L$',color='m',fontsize=16)
plt.xlim([-1.,1.])
titleHeader='First 9 Turns: $\Omega/\omega_L=$%5.3f, $ro/ro_{crit}=$%5.3f'
plt.title(titleHeader % (Omega_omega_L[2],ro_roCrit[2]),color='m',fontsize=16)
plt.grid(True)
plt.axes().set_aspect('equal')
   
fig110=plt.figure(110)
plt.plot(x[0*N_ppt:1*N_ppt+1,3],y[0*N_ppt:1*N_ppt+1,3],'-r',linewidth=2) 
plt.hold(True)  
plt.plot(x[1*N_ppt:2*N_ppt+1,3],y[1*N_ppt:2*N_ppt+1,3],'-b',linewidth=2) 
plt.plot(x[2*N_ppt:3*N_ppt+1,3],y[2*N_ppt:3*N_ppt+1,3],'-m',linewidth=2) 
plt.plot(x[3*N_ppt:4*N_ppt+1,3],y[3*N_ppt:4*N_ppt+1,3],'-g',linewidth=2) 
plt.plot(x[4*N_ppt:5*N_ppt+1,3],y[4*N_ppt:5*N_ppt+1,3],'-k',linewidth=2) 
plt.plot(x[5*N_ppt:6*N_ppt+1,3],y[5*N_ppt:6*N_ppt+1,3],'-xr',linewidth=2,markersize=10) 
plt.plot(x[6*N_ppt:7*N_ppt+1,3],y[6*N_ppt:7*N_ppt+1,3],'-xb',linewidth=2,markersize=10) 
plt.plot(x[7*N_ppt:8*N_ppt+1,3],y[7*N_ppt:8*N_ppt+1,3],'-xm',linewidth=2,markersize=10) 
plt.plot(x[8*N_ppt:9*N_ppt+1,3],y[8*N_ppt:9*N_ppt+1,3],'-xg',linewidth=2,markersize=10) 
plt.xlabel('$x/ro_L$',color='m',fontsize=16)
plt.ylabel('$y/ro_L$',color='m',fontsize=16)
titleHeader='First 9 Turns: $\Omega/\omega_L=$%5.3f, $ro/ro_{crit}=$%5.3f'
plt.title(titleHeader % (Omega_omega_L[3],ro_roCrit[3]),color='m',fontsize=16)
plt.grid(True)
plt.axes().set_aspect('equal')
   
fig120=plt.figure(120)
plt.plot(x[0*N_ppt:1*N_ppt+1,0],y[0*N_ppt:1*N_ppt+1,0],'-r',linewidth=2) 
plt.hold(True)  
plt.plot(x[0*N_ppt:1*N_ppt+1,1],y[0*N_ppt:1*N_ppt+1,1],'-b',linewidth=2) 
plt.plot(x[0*N_ppt:1*N_ppt+1,2],y[0*N_ppt:1*N_ppt+1,2],'-m',linewidth=2) 
plt.plot(x[0*N_ppt:1*N_ppt+1,3],y[0*N_ppt:1*N_ppt+1,3],'-g',linewidth=2) 
plt.xlabel('$x/ro_L$',color='m',fontsize=16)
plt.ylabel('$y/ro_L$',color='m',fontsize=16)
plt.title( \
'First Turn for Different $ro/ro_{crit}$ with $ro_{crit}=[Z_ie^2/(m\omega_L^2)]^{1/3}$', \
          color='m',fontsize=16)
plt.legend([('%5.3f' % ro_roCrit[0]),('%5.3f' % ro_roCrit[1]), \
            ('%5.3f' % ro_roCrit[2]),('%5.3f' % ro_roCrit[3]),], \
          fontsize=16,loc='upper left')
plt.grid(True)
plt.axes().set_aspect('equal')
   

#
# "Radius of the "orbital torus":
#   
maxLogRho_s=0.7
minLogRho_s=0.
pointsLog10_s=50
log10Rho_s=np.zeros(pointsLog10_s)
rhoCrrnt_s=np.zeros(pointsLog10_s)
omega_z_s=np.zeros(pointsLog10_s)
Omega_s=np.zeros(pointsLog10_s)
relOmegas_s=np.zeros(pointsLog10_s)
radiusTorus_ro=np.zeros(pointsLog10_s)

print 'ro_larm=%e, ro_crit=%e' % (ro_larm,rhoCrit)

for i in range(pointsLog10_s):
   log10Rho_s[i]=minLogRho_s+(maxLogRho_s-minLogRho_s)/(pointsLog10_s-1)*i
   rhoCrrnt_s[i]=rhoCrit*math.pow(10.,log10Rho_s[i])
   omega_z_s[i]=np.sqrt(q_elec**2/(m_elec*rhoCrrnt_s[i]**3))
   Omega_s[i]=np.sqrt(omega_L**2+4.*omega_z_s[i]**2)
   relOmegas_s[i]=omega_z_s[i]/Omega_s[i]
   radiusTorus_ro[i]=.5*(1.-np.sqrt(1.-4.*relOmegas_s[i]**2))
#   print 'i=%d, rhoCrrnt_s=%e,rhoCrrnt_s/rhoCrit=%e, widthTorus_ro=%e' % \
#         (i,rhoCrrnt_s[i],log10Rho_s[i],radiusTorus_ro[i])

fig35=plt.figure(35)
plt.plot(rhoCrrnt_s/rhoCrit,radiusTorus_ro,'-r',linewidth=2)   
plt.hold(True)  
plt.xlabel('Impact Parameter: $ro/ro_{crit}$',color='m',fontsize=16)
plt.ylabel('$\Delta_r$',color='m',fontsize=16)
plt.xlim([.95,5.05])
plt.title('$\Delta_r=0.5\cdot\Delta ro/ro_L=0.5\cdot[1-(|r(t)|/ro_L)|_{min}]$', \
color='m',fontsize=16)
plt.grid(True)
plt.text(1.5,.25, '$\Delta_r=0.5\cdot$',color='m',fontsize=20)
plt.plot([2.24,2.85-.25],[.254,.254],'-m',linewidth=1)   
plt.text(2.2525,.2575,'$\Delta ro$',color='m',fontsize=20)
plt.text(2.315,.245,'$ro_L$',color='m',fontsize=20)
plt.text(2.6,.25,'$=0.5\cdot(1-[$',color='m',fontsize=20)
plt.plot([3.45,4.49],[.254,.254],'-m',linewidth=1)   
plt.text(3.45,.235,'$4+ro^3/ro_{crit}^3$',color='m',fontsize=20)
plt.text(3.62,.26,'$ro^3/ro_{crit}^3$',color='m',fontsize=20)
plt.text(4.495,.25,'$]^{1/2})$',color='m',fontsize=20)
   
#
# Plot for maximamal impact parameter R_shield:
#   
tempL=eVtoErg*1.e-4

pointsDens=20
densElec=np.zeros(pointsDens)

minDensElec=1.e7
maxDensElec=1.e9
log10minDens=math.log10(minDensElec)
log10maxDens=math.log10(maxDensElec)

for i in range(pointsDens):
   log10crrnt=log10minDens+(log10maxDens-log10minDens)/(pointsDens-1)*i
   densElec[i]=math.pow(10,log10crrnt)                             # cm^-3

# print 'densElec: ', densElec

neutR=np.zeros(pointsDens)
debyeR=np.zeros(pointsDens)

for i in range(pointsDens):
   neutR[i]=1e4*math.pow(.75/densElec[i],1./3.)                    # mkm 
   debyeR[i]=1e4*np.sqrt(tempL/(2*pi*q_elec**2*densElec[i]))       # mkm

# print 'densElec, debyeR: ', debyeR,densElec

pointsVrel=100
velRel=np.zeros(pointsVrel)
neutRcrrnt=np.zeros((pointsVrel,pointsDens))
debyeRcrrnt=np.zeros((pointsVrel,pointsDens))
roMaxCrrnt=np.zeros((pointsVrel,pointsDens))

maxVrel=4.

for j in range(pointsDens):
   for i in range(pointsVrel):
      velRel[i]=maxVrel*i/pointsVrel                               # dimensionless
      neutRcrrnt[i,j]=neutR[j]
      debyeRcrrnt[i,j]=debyeR[j]*velRel[i]                         # mkm
      if velRel[i] < 1: 
         debyeRcrrnt[i,j]=debyeR[j]                                # mkm

for j in range(pointsDens):
   for i in range(pointsVrel):
      roMaxCrrnt[i,j]=max(neutRcrrnt[i,j],debyeRcrrnt[i,j])        # mkm


fig130=plt.figure(130)
plt.plot(velRel,debyeRcrrnt[:,0],'-r',linewidth=2)
plt.hold(True)  
plt.plot(velRel,debyeRcrrnt[:,10],'-m',linewidth=2)
plt.plot(velRel,debyeRcrrnt[:,pointsDens-1],'-b',linewidth=2)
plt.plot(velRel,neutRcrrnt[:,0],'--r',linewidth=2)
plt.plot(velRel,neutRcrrnt[:,10],'--m',linewidth=2)
plt.plot(velRel,neutRcrrnt[:,pointsDens-1],'--b',linewidth=2)
plt.xlabel('Relative Velocity $V/\Delta_{||}$',color='m',fontsize=16)
plt.ylabel('$R_D$ & $R_z$, $\mu$m',color='m',fontsize=16)
plt.title('$R_D=V_i/\Delta_{||} \cdot [T_{||} /(2 \pi e^2 n_e)]^{1/2}$, $R_z=[3Z_i/(4n_e)]^{1/3}$', \
          color='m',fontsize=16)
plt.legend(['$R_D$ ($n_e=10^7$ cm$^{-3}$)','$R_D$ ($n_e=10^8$ cm$^{-3}$)','$R_D$ ($n_e=10^9$ cm$^{-3}$)', \
            '$R_z$ ($n_e=10^7$ cm$^{-3}$)','$R_z$ ($n_e=10^8$ cm$^{-3}$)','$R_z$ ($n_e=10^9$ cm$^{-3}$)'], \
            fontsize=16,loc='upper left')
plt.grid(True)


fig140=plt.figure(140)
plt.plot(velRel,roMaxCrrnt[:,0],'-r',linewidth=2)
plt.hold(True)  
plt.plot(velRel,roMaxCrrnt[:,10],'-m',linewidth=2)
plt.plot(velRel,roMaxCrrnt[:,pointsDens-1],'-b',linewidth=2)
plt.xlabel('Relative Velocity $V/\Delta_{||}$',color='m',fontsize=16)
plt.ylabel('$R_{shield}$, $\mu$m',color='m',fontsize=16)
plt.title('$R_{shield}$=max{$R_z,R_D$}',color='m',fontsize=16)
plt.legend(['$n_e=10^7$ cm$^{-3}$','$n_e=10^8$ cm$^{-3}$','$n_e=10^9$ cm$^{-3}$'], \
            fontsize=16,loc='upper left')
plt.grid(True)


minDensElec=1.e7
maxDensElec=1.e8
log10minDens=math.log10(minDensElec)
log10maxDens=math.log10(maxDensElec)

for i in range(pointsDens):
   log10crrnt=log10minDens+(log10maxDens-log10minDens)/(pointsDens-1)*i
   densElec[i]=math.pow(10,log10crrnt)                             # cm^-3

# print 'densElec: ', densElec

neutR=np.zeros(pointsDens)
debyeR=np.zeros(pointsDens)

for i in range(pointsDens):       # mkm
   neutR[i]=1e4*math.pow(.75/densElec[i],1./3.)                    # mkm
   debyeR[i]=1e4*np.sqrt(tempL/(2*pi*q_elec**2*densElec[i]))       # mkm

pointsVrel=100
velRel=np.zeros(pointsVrel)
neutRcrrnt=np.zeros((pointsVrel,pointsDens))
debyeRcrrnt=np.zeros((pointsVrel,pointsDens))
roMaxCrrnt=np.zeros((pointsVrel,pointsDens))

maxVrel=4.

for j in range(pointsDens):
   for i in range(pointsVrel):
      velRel[i]=maxVrel*i/pointsVrel                               # dimensuionless 
      neutRcrrnt[i,j]=neutR[j]                                     # mkm
      debyeRcrrnt[i,j]=debyeR[j]*velRel[i]                         # mkm
      if velRel[i] < 1: 
         debyeRcrrnt[i,j]=debyeR[j]                                # mkm

for j in range(pointsDens):
   for i in range(pointsVrel):
      roMaxCrrnt[i,j]=max(neutRcrrnt[i,j],debyeRcrrnt[i,j])        # mkm


X,Y=np.meshgrid(densElec,velRel)      
fig150=plt.figure(150)
ax150=fig150.gca(projection='3d')
surf=ax150.plot_surface(X,Y,roMaxCrrnt,cmap=cm.coolwarm,linewidth=0,antialiased=False)
plt.title('$R_{shield}$=max{$R_z,R_D$}', color='m',fontsize=20)
plt.xlabel('$n_e$, cm$^{-3}$',color='m',fontsize=16)
plt.ylabel('$V/\Delta_{||}$',color='m',fontsize=16)
ax150.set_zlabel('$R_{shield}$, $\mu$m',color='m',fontsize=16)
fig150.colorbar(surf, shrink=0.5, aspect=5)
plt.grid(True)

minDensElec=1.e8
maxDensElec=1.e9
log10minDens=math.log10(minDensElec)
log10maxDens=math.log10(maxDensElec)

for i in range(pointsDens):
   log10crrnt=log10minDens+(log10maxDens-log10minDens)/(pointsDens-1)*i
   densElec[i]=math.pow(10,log10crrnt)                             # cm^-3

# print 'densElec: ', densElec

neutR=np.zeros(pointsDens)
debyeR=np.zeros(pointsDens)

for i in range(pointsDens):
   neutR[i]=1e4*math.pow(.75/densElec[i],1./3.)
   debyeR[i]=1e4*np.sqrt(tempL/(2*pi*q_elec**2*densElec[i]))

pointsVrel=100
velRel=np.zeros(pointsVrel)
neutRcrrnt=np.zeros((pointsVrel,pointsDens))
debyeRcrrnt=np.zeros((pointsVrel,pointsDens))
roMaxCrrnt=np.zeros((pointsVrel,pointsDens))

maxVrel=4.

for j in range(pointsDens):
   for i in range(pointsVrel):
      velRel[i]=maxVrel*i/pointsVrel                               # dimensuionless
      neutRcrrnt[i,j]=neutR[j]                                     # mkm
      debyeRcrrnt[i,j]=debyeR[j]*velRel[i]                         # mkm
      if velRel[i] < 1: 
         debyeRcrrnt[i,j]=debyeR[j]                                # mkm

for j in range(pointsDens):
   for i in range(pointsVrel):
      roMaxCrrnt[i,j]=max(neutRcrrnt[i,j],debyeRcrrnt[i,j])        # mkm


X,Y=np.meshgrid(densElec,velRel)      
fig160=plt.figure(160)
ax160=fig160.gca(projection='3d')
surf=ax160.plot_surface(X,Y,roMaxCrrnt,cmap=cm.coolwarm,linewidth=0,antialiased=False)
plt.title('$R_{shield}$=max{$R_z,R_D$}', color='m',fontsize=20)
plt.xlabel('$n_e$, cm$^{-3}$',color='m',fontsize=16)
plt.ylabel('$V/\Delta_{||}$',color='m',fontsize=16)
ax160.set_zlabel('$R_{shield}$, $\mu$m',color='m',fontsize=16)
fig160.colorbar(surf, shrink=0.5, aspect=5)
plt.grid(True)

plt.show()   

'''  
fig5.savefig('picturesKME/magnetizationArea_vs_Bfield_fig5kme.jpg')    
fig30.savefig('picturesKME/omegaZ_vs_impctPrmtr_fig30kme.jpg')    
fig35.savefig('picturesKME/torusRadius_vs_impctPrmtr_fig35kme.jpg')  
fig50.savefig('picturesKME/Omega_vs_impctPrmtr_fig50kme.jpg')    
fig55.savefig('picturesKME/Omega_vs_impctPrmtr_zoom_fig55kme.jpg')    
'''  
fig70.savefig('picturesKME/relativeR_vs_time_fig70kme.jpg')    
fig75.savefig('picturesKME/relativeR_vs_time_spec_fig75kme.jpg')    
'''  
fig80.savefig('picturesKME/nineTurns_relRo_49e-5_fig80kme.jpg')    
fig90.savefig('picturesKME/nineTurns_relRo_62e-5_fig90kme.jpg')    
fig100.savefig('picturesKME/nineTurns_relRo_103e-5_fig100kme.jpg')    
fig110.savefig('picturesKME/nineTurns_relRo_29e-3_fig110kme.jpg')    
fig120.savefig('picturesKME/fistTurn_different-relRo_fig120kme.jpg')    
'''

sys.exit()   
