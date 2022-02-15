# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 06:21:37 2022

@author: Eric.Honert
"""

#______________________________________________________________________________
# Import selected libraries here
from fitparse import FitFile
import pandas as pd
import matplotlib.pyplot as plt

fitfile = FitFile('Running_2022-02-09T17_50_14.fit')

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
                
                
