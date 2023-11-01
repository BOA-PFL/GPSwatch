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

# Read in files
# only read .asc files for this work
fPath = 'C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\WatchData\\'
# fPath = 'C:\\Users\\eric.honert\\OneDrive - Boa Technology Inc\\Documents\\Projects\\2022_TrialRun\\TestData\GPS\\'
fileExt = r".csv"
entries = [fName for fName in os.listdir(fPath) if fName.endswith(fileExt)]
# Variable for saving
save_on = 1

# Preallocate
Subject = []
Config = []
Sesh = []

s1_time = []
s1_avgspeed = []
s1_avghr = []
s1_avgpwr = []
s1_end = []

s2_time = []
s2_avgspeed = []
s2_avghr = []
s2_avgpwr = []
s2_start = []
s2_end = []

s3_time = []
s3_avgspeed = []
s3_avghr = []
s3_avgpwr = []
s3_start = []

sO_time = []


for ii in range(0,len(entries)):
    # Load the selected fit file
    df = pd.read_csv(fPath+entries[ii])
    # Convert the newly loaded timestamps
    df.timestamp  = pd.to_datetime(df.timestamp)
    # Extract file information
    Subject.append(entries[ii].split(sep = "_")[0])
    Config.append(entries[ii].split(sep = "_")[1])
    Sesh.append(entries[ii].split(sep = "_")[2][0])    
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
    idx_start_trial = np.where(df.speed > 0)[0][0]-1
    # idx_start_trial = 0
    
    if ii == 52:
        idx_end = 241
    else:
        idx_end = np.nanargmin(seg_lat)
    
    if ii == 104:
        s1_time.append(207)
        s1_end.append(205)
        s1_avgspeed.append(np.nan)
        s1_avghr.append(np.nan)
        s1_avgpwr.append(np.nan) 
    else:
        s1_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start_trial].timetuple()))
        s1_end.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start_trial].timetuple())-2)
        s1_avgspeed.append(np.nanmean(df.speed[idx_start_trial:idx_end]))
        s1_avghr.append(np.nanmean(df.heart_rate[idx_start_trial:idx_end]))
        s1_avgpwr.append(np.nanmean(df.power[idx_start_trial:idx_end]))   
    
    #__________________________________________________________________________
    # Segment 2: Top Technical Section
    if ii== 52:
        idx_start = 465
    else: 
        idx_start = idx_end
    
    if ii == 104:
        s2_time.append(np.nan)
        s2_start.append(217)
        s2_end.append(455)
        s2_avgspeed.append(np.nan)
        s2_avghr.append(np.nan)
        s2_avgpwr.append(np.nan)
    else:
        idx_end = np.nanargmax(seg_lat)
        s2_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
        s2_start.append(time.mktime(df.timestamp[idx_start].timetuple())-time.mktime(df.timestamp[idx_start_trial].timetuple())+2)
        s2_end.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start_trial].timetuple())-2)
        s2_avgspeed.append(np.nanmean(df.speed[idx_start:idx_end]))
        s2_avghr.append(np.nanmean(df.heart_rate[idx_start:idx_end]))
        s2_avgpwr.append(np.nanmean(df.power[idx_start:idx_end]))
    
    #__________________________________________________________________________
    # Segment 3: Downhill
    idx_start = idx_end
    idx_end = np.where(df.speed > 0)[0][-1]
    # If statement regarding the end of the trial
    idx_dist = np.where(df.distance > 1600)
    idx_speed = np.where(df.speed[idx_dist[0]] == 0)
    if len(idx_speed[0]) > 0:
        idx_end = idx_dist[0][idx_speed[0][0]]-1
    else: 
        idx_end = np.where(df.speed > 0)[0][-1]
    
    if ii == 104:
        s3_time.append(np.nan)
        s3_start.append(465)
        s3_avgspeed.append(np.nan)
        s3_avghr.append(np.nan)
        s3_avgpwr.append(np.nan)
    else:
        s3_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
        s3_start.append(time.mktime(df.timestamp[idx_start].timetuple())-time.mktime(df.timestamp[idx_start_trial].timetuple())+2)
        s3_avgspeed.append(np.nanmean(df.speed[idx_start:idx_end]))
        s3_avghr.append(np.nanmean(df.heart_rate[idx_start:idx_end]))
        s3_avgpwr.append(np.nanmean(df.power[idx_start:idx_end]))
    
    
    #__________________________________________________________________________
    # Overall
    idx_start = np.where(df.speed > 0)[0][0]-1
    # idx_start = 0
    if ii == 104:
        sO_time.append(615)
    else:
        sO_time.append(time.mktime(df.timestamp[idx_end].timetuple())-time.mktime(df.timestamp[idx_start].timetuple()))
    
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')  

outcomes = pd.DataFrame({'Subject':list(Subject), 'Config': list(Config),'Sesh': list(Sesh), 'TimeOverall': list(sO_time),
                          'TimeS1': list(s1_time), 'EndS1': list(s1_end), 'AvgSpeedS1':list(s1_avgspeed),'AvgHRS1':list(s1_avghr),
                          'AvgPowerS1':list(s1_avgpwr),'TimeS2': list(s2_time), 'StartS2': list(s2_start), 'EndS2': list(s2_end), 'AvgSpeedS2':list(s2_avgspeed),'AvgHRS2':list(s2_avghr),
                          'AvgPowerS2':list(s2_avgpwr),'TimeS3': list(s3_time), 'StartS3': list(s3_start), 'AvgSpeedS3':list(s3_avgspeed),'AvgHRS3':list(s3_avghr),
                          'AvgPowerS3':list(s3_avgpwr)})     

if save_on == 1:          
    outcomes.to_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\CombinedGPS.csv',header=True)