# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:07:06 2022

@author: Eric.Honert
"""
#This code converts fit files and combines all GPS outcomes (Top speed, avg speed, subject name, Trial number) into a csv
#______________________________________________________________________________
# Import selected libraries here

import pandas as pd
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import os
#import addcopyfighandler
from tkinter import messagebox

save_on = 1
debug = 1

# Set the directory for the files
fPath = 'Z:\\Testing Segments\\Snow Performance\\2024\\EH_Snowboard_BurtonWrap_Perf_Dec2024\\RaceBoxGPS\\'
entries = [fName for fName in os.listdir(fPath) if fName.endswith('.csv')]

#trial_order = pd.read_excel(fPath + 'TrialOrder_2024.xlsx')


# Preallocate
TopSpeed = []
AvgSpeed = []
sName = []
cName = []
TrialNo = []

badFileList = []
#__________________________________________________________________________
# Extract the fitfile information into dataframe (df)
for ii in range(0,len(entries)):
    
    #ii = 1
    
    if 'utcomes' not in (entries[ii]):
        print(entries[ii])
        gpsfile = pd.read_csv(fPath + entries[ii])
        
        tmpSub = entries[ii].split(sep = "_")[0]
        tmpConf = entries[ii].split(sep = "_")[1]
        firstRun = int(entries[ii].split(sep = "_")[2])
        
        # Get the subject trial order:
        
        
       
        
        # Find the top of each run
        peak_loc,peakheights = sig.find_peaks(gpsfile.Altitude,height=3000,distance=5000)
        print(len(peak_loc))
        
        
       
        
        for count, jj in enumerate(peak_loc):
            try:
                    # count = 1
                    # jj = peak_loc[count]
                    
                    # Look in a +/- 30 sec window range to find when the speed crosses 20 kph
                    idx = gpsfile.KPH[jj:jj+500] > 20
                    if sum(idx) == 0:
                        # Increase search area if faster speed not detected
                        idx = gpsfile.KPH[jj:jj+5000] > 20 
                    # Find where the subject is skiing
                    start_ski = np.where(idx==True)[0][0]+jj
                    
                    answer = True # Defaulting to true: In case "debug" is not used
                    if debug == 1:
                        plt.figure()
                        plt.plot(gpsfile.Altitude)
                        plt.plot(start_ski, gpsfile.Altitude[start_ski], 'rx')
                        answer = messagebox.askyesno("Question","Is data clean?")
                       
                        saveFolder = fPath + 'AltitudePlots'
                        
                        if answer == True:
                            if os.path.exists(saveFolder) == False:
                                os.mkdir(saveFolder)  
                            plt.savefig(saveFolder + '/' + entries[ii].split[0] + entries[ii].split(sep="_")[1]  +'.png')
                         
                       
                        plt.close()
                        if answer == False:
                            print('Adding file to bad file list')
                            
                    
                    if answer == True:
                    
                        idx = gpsfile.Altitude[start_ski:start_ski+2000]-gpsfile.Altitude[start_ski] > -100 # Look at 100m vertical of skiing
                        ski_idx = np.where(idx==True)[0] + start_ski
                        TopSpeed.append(max(gpsfile.KPH[ski_idx]))
                        AvgSpeed.append(np.mean(gpsfile.KPH[ski_idx]))
                        sName.append(tmpSub)
                        cName.append(tmpConf)
                        TrialNo.append(firstRun + count)
            except:
                print('Skipping a Run')
                        

outcomes = pd.DataFrame({'Subject':list(sName),'Config': list(cName),'trialNo': list(TrialNo),'TopSpeed':list(TopSpeed),'AvgSpeed':list(AvgSpeed)})


outfileName = fPath + '1_GPSOutcomes.csv'
if save_on == 1:
    if os.path.exists(outfileName) == False:
        
        outcomes.to_csv(outfileName, header=True, index = False)

    else:
        outcomes.to_csv(outfileName, mode='a', header=False, index = False) 

