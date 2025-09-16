#Author: Samhita Mallavarapu

#This is a Python Script that extracts scaling ratios of neuron branches that 
#takes a standard neuron reconstruction in the swc format as an input.
#This standard reconstruction has a list of pixels with coordinates and radius
#This script takes this data and organizes it in branches with branch and parent labels
#From this, it calculates the radius and length scaling ratios
#To run this code in the terminal, write python swc-to-ratios.py filename.swc label
#The label is so that you can use this to run on multiple swc files in the same directory
#The output files for scaling ratios will have a respective number labelling, such as a number labelling

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import os
import sys


#This block takes the file and counts the number of numerical entries, or pixels

numlines = 0

with open(sys.argv[1]) as f:
  for line in f:
   if line != '/n' and not line.startswith('#'):
       numlines += 1

print(numlines)

data = np.loadtxt(sys.argv[1])

pix_id = data[0:numlines, 0] #extracts the pixel ID number from the file
art_id = data [0:numlines, 1] #extracts the identifier/type where 1 is soma, 2 is axon, 3 is a basal dendrite, and 4 is an apical dendrite
x = data [0:numlines, 2] #extracts the x spatial coordinate
y = data [0:numlines, 3] #extracts the y spatial coordinate
z = data [0:numlines, 4] #extracts the z spatial coordinate
radius = data [0:numlines, 5] #extracts the radius at that coordinate
pix_par_id = data [0:numlines, 6] #extracts the parent pixel


pix_par_id[0] = 0 #sets the first parent pixel to be 0

#Extracts the pixel IDs where branches occur

branching_id = np.zeros(numlines)

count1 = 0

for i in range (numlines):
    if (pix_id[i] - pix_par_id[i]) > 2: #Find where there is a gap between pixel and parent
        branching_id[count1] = branching_id[count1] + pix_id[i]
    if branching_id[count1] != 0:
        count1 = count1 + 1

#Here, we find the child pixel IDs where the branchings occur and the pixel IDs of the parent IDs
#each parent ID is associated with at least two separate child IDs

pix_child_id = np.zeros(numlines)

pix_child_parent_id = np.zeros(numlines)

count2 = 0

for j in range(count1): 
    for i in range(numlines):
        if pix_par_id[int(branching_id[j])-1] == pix_par_id[i]: #Finds the parents of where the branches occur
            pix_child_parent_id[count2] = pix_par_id[i]
            pix_child_id[count2] = i+1 #Finds where the children of the parents occur
            count2 = count2 + 1

#separates the branches 
vessel_id = np.zeros(numlines)

vessel_id[0] = 1
vessel_id[1] = 1

count3 = 1

for i in range(2,numlines):
    for j in range(count2):
        if pix_id[i] == pix_child_id[j]: #If this is where one of the branchinds occur
            count3 = count3 + 1
            break
    vessel_id[i] = count3

vessel_parent_id_list = np.zeros(numlines)

#Extraction of parent ids


for j in range(numlines):
    if vessel_id[j] == 1:
      vessel_parent_id_list[j] = 1
    for i in range(count2):       
        if pix_id[j] == pix_par_id[int(pix_child_id[i])-1]: #Finds where the parents of the branches occur
            vessel_parent_id_list[j] = vessel_id[j]

for k in range(numlines):
    if vessel_parent_id_list[k]==0:
        for j in range(k):
            if pix_par_id[k] == j+1 : #For the remaining parent IDs not identified by branches, finds the parent pixels and labels the vessel parent IDs as the same, as they adjacent and in the same vessel
                vessel_parent_id_list[k] = vessel_parent_id_list[j]
               

#Breaks up the parents vessels into levels

vessel_parent_id = np.zeros(count3)

vessel_parent_id[0] = 1
count4 = 1

for j in range(1,numlines):
    if count4 == count3:
       break
    vessel_parent_id[count4] = vessel_parent_id_list[j+1] #labels parent vessels
    if vessel_id[j] != vessel_id[j+1] and vessel_id[j+1] != vessel_id[j+2]: #Deals with the case that a branch is only one pixel long
        vessel_parent_id[count4] = vessel_parent_id_list[j]
    if vessel_id[j] != vessel_id[j+1]: #if these is a break in vessels
        count4 = count4+1      

#Creates the output file, with 4 columns, organized by branch/"vessel"

swc_output = np.zeros((count3, 4))

#Just labels in order
for i in range(count3):
    swc_output[i,0] = i +1
    
#Parents
for i in range(count3):
    swc_output[i,1] = vessel_parent_id[i] #Labels parents in the output so the ratio can be found
    
    
for j in range(count3):
    radius_avg_j = 0
    count4_j = 0
    for i in range(numlines):
        if vessel_id[i] == j+1: 
            count4_j = count4_j +1
            radius_avg_j = radius_avg_j + radius[i] #Sums up randius in a branch
    if count4_j != 0:
        radius_avg_j = radius_avg_j/count4_j #Divides by the total number to find the average
    if count4_j == 0:
        radius_avg_j = radius_avg_j/1
    swc_output[j,2] = swc_output[j,2] + radius_avg_j #Finds the average radius for the output in each branch
    
for j in range(count3):
    length_j = 0
    for i in range(numlines-1):
        if vessel_id[i] == j+1 and vessel_id[i+1] == j+1: 
            length_j = length_j + math.sqrt((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2 + (z[i+1]-z[i])**2) #Finds length by the euclidean distance between pixels
    swc_output[j,3] = swc_output[j,3] + length_j


#Getting the ratios

ratios = np.zeros((count3, 3))

#Print in first column the parent branch of the ratio, ie, n+1 

for i in range(count3):
    ratios[i,0] = i+1
    for j in range(count3):
        if swc_output[i,0] == swc_output[j,1] and swc_output[i,2] != 0 and swc_output[i,3]!= 0: #j denotes the daughter branch; checking to see if its parent i exists and finding the corresponding daughter to parent ratio 
            ratios[i,1] = swc_output[j,2]/swc_output[i,2] #radius ratio
            ratios[i,2] = swc_output[j,3]/swc_output[i,3] #length ratio
            
count4 = 0
for i in range(count3):
    if ratios[i,1] != 0 and ratios[i,2] != 0: #total number of branches with nonzero ratios
        count4 = count4 + 1

#Need one less than the total number of branches

radius_ratio_list = np.zeros(count4-1)
length_ratio_list = np.zeros(count4-1) 

count5 = 0 

for i in range(1,count3):
    if ratios[i,1] != 0 and ratios[i,2] != 0:
        radius_ratio_list[count5] = ratios[i,1]
        length_ratio_list[count5] = ratios[i,2]
        count5 = count5 + 1


#If at any point the code does not work, can remove comment to save files that have printed intermediate steps 

#np.savetxt('pix_id.dat', pix_id)
#np.savetxt('pix_par_id.dat', pix_par_id)
#np.savetxt('pix_child_id.dat', pix_child_id)
#np.savetxt('pix_child_parent_id.dat', pix_child_parent_id)
#np.savetxt('branching_id.dat', branching_id)
#np.savetxt('vessel_id.dat', vessel_id)
#np.savetxt('vessel_parent_id_list.dat', vessel_parent_id_list)
#np.savetxt('vessel_parent_id.dat', vessel_parent_id)
#np.savetxt('ratios.dat', ratios)

#Final output: Angicart-style output (arranged by branch) and list of ratios 

np.savetxt('swc_output_%s.dat'% sys.argv[2], swc_output)
np.savetxt('radius_ratio_list_%s.dat'% sys.argv[2], radius_ratio_list)
np.savetxt('length_ratio_list_%s.dat'% sys.argv[2], length_ratio_list)
