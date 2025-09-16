#Author: Samhita Mallavarapu

import pandas as pd

import numpy as np



rad1 = np.loadtxt('radius_ratio_list_MTG6.dat') #might need to change label

rad2 = np.loadtxt('radius_ratio_list_MTG6.1.dat')

rad3 = np.loadtxt('radius_ratio_list_MTG6.2.dat')



len1 = np.loadtxt('length_ratio_list_MTG6.dat')

len2 = np.loadtxt('length_ratio_list_MTG6.1.dat')


len3 = np.loadtxt('length_ratio_list_MTG6.2.dat')




vert_stack = np.concatenate((rad1, rad2, rad3), axis=None)


vert_stack2 = np.concatenate((len1, len2, len3), axis=None)



np.savetxt('combinedrad.dat', vert_stack)


np.savetxt('combinedlen.dat', vert_stack2)
