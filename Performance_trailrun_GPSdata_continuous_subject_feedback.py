# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 06:21:37 2022

@author: Eric.Honert
"""

#This code gets GPS results for 1 participant at a time. Use when wanting to look just at one person's data

#______________________________________________________________________________
# Import selected libraries here
from fitparse import FitFile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time
import addcopyfighandler
from tkinter.filedialog import askopenfilename




# Preallocate
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
filename = askopenfilename()

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

#__________________________________________________________________________
# Segment the data into the number of expected loops

# Expecting 3 loops: find the two points where the watch was paused then restarted
watch_time = np.array([datetime.timestamp(ts) for ts in df.timestamp])
watch_time = watch_time-watch_time[0]

# Examine the watch time for when there is a break of over 100 seconds in the time
splits, = np.where(np.diff(watch_time)> 100)
print(len(splits)+1,' Laps Detected')

for jj in range(len(splits)+1):
    if jj == 0:
        subdf = df.iloc[0:splits[jj]+1,:]
    elif jj == len(splits):
        subdf = df.iloc[splits[jj-1]+2:,:]
    else:
        subdf = df.iloc[splits[jj-1]+2:splits[jj]+1,:]
    
    subdf = subdf.reset_index(drop = True)
    subdf.distance = subdf.distance - subdf.distance[0]
    #__________________________________________________________________________
    # Indicate the top of the trail to find the different portions of the run
    # The longitude that it should be greater than was found through guess and check
    idx = subdf.position_long < -1255001500.0
    
    seg_long = np.array(subdf.position_long)+0.0 # adding 0.0 is just to make sure that the array is float
    seg_long[idx] = np.nan
    seg_lat = np.array(subdf.position_lat)+0.0 # adding 0.0 is just to make sure that the array is float
    seg_lat[idx] = np.nan
    #__________________________________________________________________________
    # Segment 1: Uphill
    idx_start_trial = np.where(df.cadence > 0)[0][0]-1
    # idx_start = 0
    idx_end = np.nanargmin(seg_lat)
    s1_time.append(time.mktime(subdf.timestamp[idx_end].timetuple())-time.mktime(subdf.timestamp[idx_start_trial].timetuple()))
    s1_avgspeed.append(1/(np.nanmean(subdf.speed[idx_start_trial:idx_end])*60/1609.34))
    s1_avghr.append(np.nanmean(subdf.heart_rate[idx_start_trial:idx_end]))
    s1_avgpwr.append(np.nanmean(subdf.power[idx_start_trial:idx_end]))
    #__________________________________________________________________________
    # Segment 2: Flat-ish
    idx_start = idx_end
    idx_end = np.nanargmax(seg_lat)
    s2_time.append(time.mktime(subdf.timestamp[idx_end].timetuple())-time.mktime(subdf.timestamp[idx_start].timetuple()))
    s2_avgspeed.append(1/(np.nanmean(subdf.speed[idx_start:idx_end])*60/1609.34))
    s2_avghr.append(np.nanmean(subdf.heart_rate[idx_start:idx_end]))
    s2_avgpwr.append(np.nanmean(subdf.power[idx_start:idx_end]))
    #__________________________________________________________________________
    # Segment 3: Downhill
    idx_start = idx_end
    idx_end = np.where(subdf.cadence > 0)[0][-1]
    # If statement regarding the end of the trial
    idx_dist = np.where(subdf.distance > 1600)
    idx_cadence = np.where(subdf.cadence[idx_dist[0]] == 0)
    if len(idx_cadence[0]) > 0:
        idx_end = idx_dist[0][idx_cadence[0][0]]-1
    else: 
        idx_end = np.where(subdf.cadence > 0)[0][-1]
    
    s3_time.append(time.mktime(subdf.timestamp[idx_end].timetuple())-time.mktime(subdf.timestamp[idx_start].timetuple()))
    s3_avgspeed.append(1/(np.nanmean(subdf.speed[idx_start:idx_end])*60/1609.34))
    s3_avghr.append(np.nanmean(subdf.heart_rate[idx_start:idx_end]))
    s3_avgpwr.append(np.nanmean(subdf.power[idx_start:idx_end]))


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