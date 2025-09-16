import numpy as np

import scipy as sp

import matplotlib.pyplot as plt

import math

import os

import sys

import csv



with open('parentname.dat','r') as file:

    filedata = file.read()

    filedata = filedata.replace('N/A','0')

with open('parentname.dat','w') as file:

    file.write(filedata)
