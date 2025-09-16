import numpy as np

import scipy as sp

from scipy import stats

import matplotlib.pyplot as plt

import math

import os

import sys

#%matplotlib inline

radius = np.loadtxt(sys.argv[1])

radius = radius[radius<1]

radius = radius[radius>0]


mean = np.mean(radius)

mean = np.around(mean, decimals =2)

std = np.std(radius)

std = np.around(std, decimals =2)

sem = sp.stats.sem(radius)

sem = np.around(sem, decimals =4)


plt.plot(1)

plt.hist(radius, bins=20, alpha = 0.75, color = 'lightpink')

plt.title('Combined Dendrite Radius Scaling Ratio Distribution', fontsize = 17)

plt.ylabel('Frequency', fontsize = 17)

plt.xlabel('Scaling Ratio', fontsize = 17)

plt.axvline(mean, color='k', linestyle = 'solid', linewidth=2)

plt.axvline(0.63, color='r', linestyle = 'dashed', linewidth=3, label = r'$\bf{P^*}$')

plt.axvline(0.71, color='g', linestyle = 'dashed', linewidth=3, label = r'$\bf{P}$')

plt.axvline(0.76, color='b', linestyle = 'dashed', linewidth=3, label = r'$\bf{T, \epsilon = 0}$')

#plt.axvline(0.79, color='m', linestyle = 'dashed', linewidth=3, label = r'$\bf{T, \epsilon = \frac{1}{2}}$$

plt.text(0.075,115, r'$\mu = %s$' % (mean), fontsize = 25)

plt.text(0.075,98, r'$SEM = %s$' % (sem), fontsize = 25)

plt.errorbar(mean, 210, xerr= 2*sem, yerr=0, fmt='.k', linewidth=2)

plt.text(0.64, 213, r'$\mu$', color = 'k', fontsize = 25)

plt.legend(loc= 'upper left', prop={'size': 20})

#plt.savefig('dendriteradius.png')


plt.savefig('histogram_radius6.0.png')
