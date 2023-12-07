# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:22:37 2022

@author: Eric.Honert

The purpose of this code is to convert a .fit file from a GPS watch to a .csv
file. This can reduce processing time (minimally) and allow for custom croping
of the .fit file.
"""

# Import libraries
from fitparse import FitFile
import pandas as pd
import os
import numpy as np

# Read in files
# only read .fit files for this work
fPath = 'C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\InLabData\\WatchData\\Raw\\'
folderExt = r""
fileExt = r".fit"
folders = [fName for fName in os.listdir(fPath) if fName.endswith(folderExt)]

trial_names = pd.read_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\InLabSubTrialOrder.csv')


Subject = []
Config = []
Label = np.array([])
Sesh = []
Speed = []
Slope = []
avgHR = []
maxHR = []
avgPower = []
maxPower = []



for ii in range(len(folders)):
    fsubPath = fPath + folders[ii] + "\\"
    entries = [fName for fName in os.listdir(fsubPath) if fName.endswith(fileExt)]
    
    timestart = []
    avgHR_tmp = []
    maxHR_tmp = []
    avgPower_tmp = []
    maxPower_tmp = []
    
    # Obtain information from trial names that are stored in temporal order    
    for trialname in trial_names.iloc[:,ii]:
        Subject.append(trialname.split(sep = "_")[0])
        Config.append(trialname.split(sep = "_")[1])
        Speed.append(trialname.split(sep = "_")[2])
        Slope.append(trialname.split(sep = "_")[3])
        Sesh.append(trialname.split(sep = "_")[4])
    
    # Extract fit file information
    for entry in entries:
        fitfile = FitFile(fsubPath+entry)
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
        avgHR_tmp.append(np.mean(df.heart_rate))
        maxHR_tmp.append(np.max(df.heart_rate))
        try:
            avgPower_tmp.append(np.mean(df.power))
            maxPower_tmp.append(np.max(df.power))
        except:
            avgPower_tmp.append(np.nan)
            maxPower_tmp.append(np.nan)
                
        
    idx = np.argsort(timestart)
    avgHR = np.concatenate((avgHR,np.array(avgHR_tmp)[idx]),axis = None)
    maxHR = np.concatenate((maxHR,np.array(maxHR_tmp)[idx]),axis = None)
    avgPower = np.concatenate((avgPower,np.array(avgPower_tmp)[idx]),axis = None)
    maxPower = np.concatenate((maxPower,np.array(maxPower_tmp)[idx]),axis = None)
    
    
outcomes = pd.DataFrame({'Subject':list(Subject), 'Config': list(Config),'Sesh': list(Sesh),
                         'Speed':list(Speed), 'Slope':list(Slope),'avgHR':list(avgHR), 'maxHR':list(maxHR),
                         'avgPower':list(avgPower),'maxPower':list(maxPower)})    
    
    
# Save the trial to a .csv
# df.to_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\WatchData\\'+entries[ii][:-4]+'.csv',header=True)
    
    