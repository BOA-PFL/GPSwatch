# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:22:37 2022

@author: Eric.Honert

The purpose of this code is to convert a .fit file from a GPS watch to a .csv
file. This can reduce processing time (minimally) and allow for custom croping
of the .fit file.
"""

# Import selected libraries here
from fitparse import FitFile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import addcopyfighandler
from tkinter.filedialog import askopenfilenames

# Preallocate
Subject = []
Config = []
Label = np.array([])
Sesh = []
Speed = []
Slope = []

s1_avghr = []
s1_avgpwr = []

s2_avghr = []
s2_avgpwr = []

s3_avghr = []
s3_avgpwr = []

avgHR = []
avgPower = []


trial_names = pd.read_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\InLabSubTrialOrder.csv')

Subject = 'IS02'

print('Open all gps files recorded for the subject')
filenames = askopenfilenames()

timestart = []
avgHR_tmp = []
maxHR_tmp = []
avgPower_tmp = []
maxPower_tmp = []

# Obtain information from trial names that are stored in temporal order    
for trialname in trial_names[Subject]:
    Config.append(trialname.split(sep = "_")[1])
    Speed.append(trialname.split(sep = "_")[2])
    Slope.append(trialname.split(sep = "_")[3])
    Sesh.append(trialname.split(sep = "_")[4])

# Extract fit file information
for entry in filenames:
    fitfile = FitFile(entry)
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
    timestart.append(df.timestamp[0])
    avgHR_tmp.append(np.nanmean(df.heart_rate))
    maxHR_tmp.append(np.max(df.heart_rate))
    try:
        avgPower_tmp.append(np.nanmean(df.power))
    except:
        avgPower_tmp.append(np.nan)
                
        
idx = np.argsort(timestart)
avgHR = np.array(avgHR_tmp)[idx]
avgPower = np.array(avgPower_tmp)[idx]
    
    
outcomes = pd.DataFrame({'Speed':list(Speed), 'Slope':list(Slope),'avgHR':list(avgHR),
                          'avgPower':list(avgPower)})

outcomes.replace(0,np.nan,inplace=True)

dum = outcomes.groupby(['Speed','Slope']).mean()

copy_data = dum.iloc[[1,2,0],:]
    
    
# Save the trial to a .csv
# df.to_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\WatchData\\'+entries[ii][:-4]+'.csv',header=True)
    
    