import numpy as np

import scipy as sp

from scipy import stats

import matplotlib.pyplot as plt

import math

import os

import sys

import csv



vesselid = np.loadtxt('vesselname.dat')

parentid = np.loadtxt('parentname.dat')

radius = np.loadtxt('vesselrad.dat')

length = np.loadtxt('vessellength.dat')



n = len(vesselid)



radratiolist = np.zeros(n)

lenratiolist = np.zeros(n)



for i in range(n):

  for j in range(n):

    if parentid[i] != 0 and parentid[i] == vesselid[j] and radius[j]!= 0 and length[j]!=0:

radratiolist[i] = radius[i]/radius[j]

        lenratiolist[i] = length[i]/radius[j]



#for i in range(948):

#  if radratiolist[i] < 0.0001:

#    radratiolist[i] = 0

#  if lenratiolist[i] < 0.0001:

#    lenratiolist[i] = 0



radratiolist = radratiolist[radratiolist != 0]

lenratiolist = lenratiolist[lenratiolist != 0]



radratiolist = radratiolist[radratiolist < 1]

lenratiolist = lenratiolist[lenratiolist < 1]

    

np.savetxt('radratios2.dat', radratiolist)

np.savetxt('lenratios2.dat', lenratiolist)



plt.rc('xtick',labelsize=17)

plt.rc('ytick',labelsize=17)





#plt.figure(1)

#plt.hist(radratiolist, bins='auto', color = 'c')

#plt.title('Angicart Radius Ratio Distribution', fontsize = 25)

#plt.ylabel('Frequency', fontsize = 18)

#plt.xlabel('Scaling Ratio', fontsize = 18)

#plt.xlim(right = 1.0)

#plt.savefig('radius_hist2.png')



#plt.figure(2)

#plt.hist(lenratiolist, bins='auto', color = 'm')

#plt.title('Angicart Length Ratio Distribution', fontsize = 25)

#plt.ylabel('Frequency', fontsize = 18)

#plt.xlabel('Scaling Ratio', fontsize = 18)

#plt.xlim(right = 1.0)

#plt.savefig('len_hist2.png')





print np.mean(radratiolist)

print np.mean(lenratiolist)



mean = np.mean(radratiolist)

mean = np.around(mean, decimals =2)

mean2 = np.mean(lenratiolist)

mean2 = np.around(mean2, decimals =2)

sem = sp.stats.sem(radratiolist)

sem = np.around(sem, decimals =3)

sem2 = sp.stats.sem(lenratiolist)

sem2 = np.around(sem, decimals =3)



plt.figure(1)

plt.hist(radratiolist, bins='auto', alpha = 0.75, color = 'gold')

plt.title('Angicart Radius Scaling Ratio Distribution', fontsize = 17)

plt.ylabel('Frequency', fontsize = 17)

plt.xlabel('Scaling Ratio', fontsize = 17)

plt.xlim(left = 0.0)

plt.axvline(mean, color='k', linestyle = 'solid', linewidth=2)

#plt.axvline(0.63, color='r', linestyle = 'dashed', linewidth=3, label = r'$\bf{P^*}$')

#plt.axvline(0.71, color='forestgreen', linestyle = 'dashed', linewidth=3, label = r'$\bf{P}$')

#plt.axvline(0.76, color='b', linestyle = 'dashed', linewidth=3, label = r'$\bf{T, \epsilon = 0}$')

#plt.axvline(0.79, color='m', linestyle = 'dashed', linewidth=3, label = r'$\bf{T, \epsilon = \frac{1}{2}}$')

plt.text(0.46,60, r'$\mu = %s$' % (mean), fontsize = 25)

#plt.text(0.35,12, r'$Median = %s$' % (median), fontsize = 25)

#plt.text(0.075,15, r'$SEM = %s$' % (sem), fontsize = 25)

#plt.text(0.62,36, r'$\bf{T, \epsilon = \frac{1}{2}}$', color='r', fontsize = 25)

plt.errorbar(mean, 10, xerr= 2*sem, yerr=0, fmt='.k', linewidth=2)

plt.text(0.45, 13, r'$\mu$', color = 'k', fontsize = 25)

#plt.legend(loc= 'upper left', prop={'size': 20})

plt.savefig('radiushistAng.png')



plt.figure(2)

plt.hist(lenratiolist, bins='auto', alpha = 0.75, color = 'lightpink')

plt.title('Angicart Length Scaling Ratio Distribution', fontsize = 17)

plt.ylabel('Frequency', fontsize = 17)

plt.xlabel('Scaling Ratio', fontsize = 17)

plt.xlim(right = 1)

plt.ylim(top = 30)

plt.axvline(mean2, color='k', linestyle = 'solid', linewidth=2)

plt.text(0.62,23, r'$\mu = %s$' % (mean2), fontsize = 25)

#plt.text(5,23, r'$Median = %s$' % (median2), fontsize = 25)

#plt.text(10,135, r'$SEM = %s$' % (sem2), fontsize = 25)

plt.errorbar(mean2, 10, xerr= 2*sem2, yerr=0, fmt='.k')

#plt.text(2.5, 90, r'$\mu$', color = 'k', fontsize = 25)

plt.savefig('lenhistAng.png')
