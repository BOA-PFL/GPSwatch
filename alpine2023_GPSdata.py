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

save_on = 1

# Set the directory for the files
fPath = 'C:\\Users\\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\Snow Performance\\SkiValidation_Dec2022\\GPS\\'
entries = [fName for fName in os.listdir(fPath) if fName.endswith('.fit')]

trial_order = pd.read_excel(fPath + 'TrialOrder.xlsx')


# Preallocate
TopSpeed = []
AvgSpeed = []
sName = []
cName = []
TrialNo = []
#__________________________________________________________________________
# Extract the fitfile information into dataframe (df)
for ii in range(0,len(entries)):
    print(entries[ii])
    fitfile = FitFile(fPath + entries[ii])
    
    tmpSub = entries[ii].split(sep = "_")[0]
    
    # Get the subject trial order:
    sub_TO = trial_order.loc[trial_order.Subject == tmpSub]
    
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
    
    for count, jj in enumerate(peak_loc):
        if sub_TO.iloc[0,count+1] != 'warmup':
            # Look in a +/- 30 sec window range to find when the speed crosses 2 m/s
            idx = df.speed[jj-30:jj+30] > 2
            # Find where the subject is skiing
            start_ski = np.where(idx==True)[0][0]+jj-30
            idx = df.distance[start_ski:]-df.distance[start_ski] < 400 # Look at 400 m of skiing
            ski_idx = np.where(idx==True)[0] + start_ski
            TopSpeed.append(max(df.speed[ski_idx]))
            AvgSpeed.append(np.mean(df.speed[ski_idx]))
            sName.append(tmpSub)
            cName.append(sub_TO.iloc[0,count+1])

outcomes = pd.DataFrame({'Subject':list(sName),'Config': list(cName),'TopSpeed':list(TopSpeed),'AvgSpeed':list(AvgSpeed)})

if save_on == 1:
    outcomes.to_csv(fPath + 'GPSOutcomes.csv',header=True)
