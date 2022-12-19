# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 06:21:37 2022

@author: Eric.Honert
"""

#______________________________________________________________________________
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
Sesh = []

s1_time = []
s1_avgspeed = []
s1_avghr = []
s1_avgpwr = []

s2_time = []
s2_avgspeed = []
s2_avghr = []
s2_avgpwr = []

s3_time = []
s3_avgspeed = []
s3_avghr = []
s3_avgpwr = []

print('Open all gps files recorded for the subject')
filenames = askopenfilenames()

for ii in range(0,len(filenames)):
    # Load the selected fit file
    fitfile = FitFile(filenames[ii])
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
    #__________________________________________________________________________
    # Indicate the top of the trail to find the different portions of the run
    # The longitude that it should be greater than was found through guess and check
    idx = df.position_long < -1255001500.0
    
    seg_long = np.array(df.position_long)+0.0 # adding 0.0 is just to make sure that the array is float
    seg_long[idx] = np.nan
    seg_lat = np.array(df.position_lat)+0.0 # adding 0.0 is just to make sure that the array is float
    seg_lat[idx] = np.nan
    #__________________________________________________________________________
    # Segment 1: Uphill
    # idx_start = np.where(df.cadence > 0)[0][0]-1
    idx_start = 0
    idx_end = np.nanargmin(seg_lat)
    s1_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
    s1_avgspeed.append(1/(np.nanmean(df.speed[idx_start:idx_end])*60/1609.34))
    s1_avghr.append(np.nanmean(df.heart_rate[idx_start:idx_end]))
    s1_avgpwr.append(np.nanmean(df.power[idx_start:idx_end]))
    #__________________________________________________________________________
    # Segment 2: Flat-ish
    idx_start = idx_end
    idx_end = np.nanargmax(seg_lat)
    s2_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
    s2_avgspeed.append(1/(np.nanmean(df.speed[idx_start:idx_end])*60/1609.34))
    s2_avghr.append(np.nanmean(df.heart_rate[idx_start:idx_end]))
    s2_avgpwr.append(np.nanmean(df.power[idx_start:idx_end]))
    #__________________________________________________________________________
    # Segment 3: Downhill
    idx_start = idx_end
    idx_end = np.where(df.cadence > 0)[0][-1]
    # If statement regarding the end of the trial
    idx_dist = np.where(df.distance > 1600)
    idx_cadence = np.where(df.cadence[idx_dist[0]] == 0)
    if len(idx_cadence[0]) > 0:
        idx_end = idx_dist[0][idx_cadence[0][0]]-1
    else: 
        idx_end = np.where(df.cadence > 0)[0][-1]
    
    s3_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
    s3_avgspeed.append(1/(np.nanmean(df.speed[idx_start:idx_end])*60/1609.34))
    s3_avghr.append(np.nanmean(df.heart_rate[idx_start:idx_end]))
    s3_avgpwr.append(np.nanmean(df.power[idx_start:idx_end]))
    
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')  

outcomes = pd.DataFrame({ 'TimeS1': list(s1_time), 'AvgSpeedS1':list(s1_avgspeed),'AvgHRS1':list(s1_avghr),
                          'AvgPowerS1':list(s1_avgpwr),'TimeS2': list(s2_time), 'AvgSpeedS2':list(s2_avgspeed),'AvgHRS2':list(s2_avghr),
                          'AvgPowerS2':list(s2_avgpwr),'TimeS3': list(s3_time), 'AvgSpeedS3':list(s3_avgspeed),'AvgHRS3':list(s3_avghr),
                          'AvgPowerS3':list(s3_avgpwr)})     

                
copy_data = np.mean(outcomes,axis = 0)
# Make sure to show min/mi in min:sec format
copy_data.AvgSpeedS1 = '%02d.%02d' % (int(copy_data.AvgSpeedS1), round(60*(copy_data.AvgSpeedS1 % 1)))
copy_data.AvgSpeedS2 = '%02d.%02d' % (int(copy_data.AvgSpeedS2), round(60*(copy_data.AvgSpeedS2 % 1)))
copy_data.AvgSpeedS3 = '%02d.%02d' % (int(copy_data.AvgSpeedS3), round(60*(copy_data.AvgSpeedS3 % 1)))
print("Copy copy_data file into athlete form")