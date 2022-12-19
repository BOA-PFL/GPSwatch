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
fPath = 'C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\WatchData\\fitFiles\\'
fileExt = r".fit"
entries = [fName for fName in os.listdir(fPath) if fName.endswith(fileExt)]


for ii in range(124,len(entries)): # 18,len(entries)
    fitfile = FitFile(fPath+entries[ii])
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
    # If cropping of the data frame needs to occur, do it here
    if ii == 17:
        df = df.iloc[0:584,:]
    elif ii == 20:
        df['power'] = np.nan
    elif ii == 83 or ii == 84 or ii == 86:
        df['power'] = np.nan
        df['cadence'] = np.nan
    elif ii == 100:
        df = df.iloc[0:467,:]
    
    # Save the trial to a .csv
    df.to_csv('C:\\Users\eric.honert\\Boa Technology Inc\\PFL Team - General\\Testing Segments\\EndurancePerformance\\TrailRun_2022\\WatchData\\'+entries[ii][:-4]+'.csv',header=True)
    
    