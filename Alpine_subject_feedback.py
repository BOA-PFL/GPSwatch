# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:07:06 2022

@author: Eric.Honert
"""

#______________________________________________________________________________
# Import selected libraries here
from fitparse import FitFile
import pandas as pd
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import os
import addcopyfighandler
from tkinter.filedialog import askopenfilename


# Read in file
# To be changed.
fPath = 'C:\\Users\\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\Snow Performance\\SkiValidation_Dec2022\\GPS\\'
filename = askopenfilename(initialdir = fPath) # Open .fit file
# Preallocate
TopSpeed = []

# Load the selected fit file
fitfile = FitFile(filename)
#__________________________________________________________________________
# Extract the fitfile information into dataframe (df)
while True:
    try:
        fitfile.messages
        break
    except KeyError:
        continue
workout = []
for record in fitfile.get_messages('record'):
    r = {}
    for record_data in record:
        r[record_data.name] = record_data.value
    workout.append(r)
df = pd.DataFrame(workout)

# Find the top of each run
peak_loc,peakheights = sig.find_peaks(df.altitude,height=3000)

# Neglect the first peak (warm-up)
for jj in peak_loc[1:]:
    # Look in a +/- 30 sec window range to find when the speed crosses 2 m/s
    idx = df.speed[jj-30:jj+30] > 2
    # Find where the subject is skiing
    start_ski = np.where(idx==True)[0][0]+jj-30
    idx = df.distance[start_ski:]-df.distance[start_ski] < 400 # Look at 500 m of skiing
    ski_idx = np.where(idx==True)[0] + start_ski
    TopSpeed.append(max(df.speed[ski_idx]))

print('Average Top Speed', round(np.mean(TopSpeed)*2.23694),'mph')
print('Subject"s top speed from each lap ranged from:')
print(round(min(TopSpeed)*2.23694),'to',round(max(TopSpeed)*2.23694),'mph')
  