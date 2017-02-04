# -*- coding: utf-8 -*-

"""
Created on Thu Jan 26 18:00 2017

@author: brad
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd   ## PANDAS is glorious and makes handling data easier, much like in R!
#from scipy import stats
from scipy import signal as sig
import BGCprocLib as bgc

## Set order for peak finding routine (Default should be 10)
Ord =  10     ## for fname1 and fname2 (use a1 to remove elements from peaksUp)
#Ord = 250     ## for fname3 and fname4
#Ord = 150     ## for fname5 and fname6
#Ord =  25     ## for fname7 and fname8 (use a2u and a2d to remove elements from peaksUp and peaksDn)
#Ord = 200     ## for fname9 and fnameA (use a3u and a3d to remove ...)
#Ord =  80     ## for fnameB and fnameC (use a4u to remove ...)

## Read the CSV data file into a data frame using PANDAS
fileAll = '../Data/05_FranckHertz_LabProData_AllTemps_UpDn.csv'
AllData = pd.read_csv(fileAll, sep=',', header=0, index_col=[0,1])
###    Col A: Temp - Temperature (C) at which the experiment was conducted
###    Col B: Dir  - Direction: 'Up' = increasing Va, 'Dn' = decreasing Va
###    Col C: Pot1 - LabPro Channel 1 potential (V) (proportional to accelerating potential)
###    Col D: Pot2 - LabPro Channel 2 potential (V) (proportional to collector current)
###################################

## The data need to be scaled according to the results found by running
## 01_FranckHertz_InitialProcessing.py
slope_Va, int_Va = (-19.096514967, -0.3912355461)
slope_Ic, int_Ic = ( -0.333075600, -0.0201979916)
AllData['Va'] = (slope_Va * AllData.Pot1) + int_Va  ## Add a column for Va
AllData['Ic'] = (slope_Ic * AllData.Pot2) + int_Ic  ## Add a column for Ic

## Smooth the accelerating potential and the collector current by FFT convolution with
## a 51-point gaussian window with a standard deviation of 20. Rollback defaults to
## 25 (half of the window).
winsize = 51 ## length of window
wintype = 1  ## gaussian window
winstdv = 20 ## standard deviation
rollbak =-25 ## amount to roll back the data after filtering (half the window length)
## Smooth the dataset

temps = [152,161,172,178,180,190]
dirs  = ['Up', 'Dn']
vaic  = ['Va', 'Ic']

## Set up a new, empty dataframe indexed on temps and dirs. Unfortunately, for now, 
## we have to set this up manually
idx = pd.MultiIndex.from_tuples([(152, 'Up'), (161, 'Up'), (172, 'Up'), (178, 'Up'), (180, 'Up'), (190, 'Up'), (152, 'Dn'), (161, 'Dn'), (172, 'Dn'), (178, 'Dn'), (180, 'Dn'), (190, 'Dn')], names=['Temps','Dirs'])
sm = pd.DataFrame(index=idx)
for i in temps:
    print("\n==================================================")
    print("processing temperature: ",i)
    for d in dirs:
        print("   processing direction: ",d)
        for v in vaic:
            print("     processing variable: ",v)
            print("        min ", v, np.min(AllData.loc[i].loc[d][v]))
            print("        max ", v, np.max(AllData.loc[i].loc[d][v]))
            sm.loc[i].loc[d][v] = bgc.funcSmoothFilt(winsize, wintype, winstdv, AllData.loc[i].loc[d][v], rollbak)
            ## This ran without error, but resulted in an empty dataframe :(
            ## I know there is a way to access locations using, say, sm.loc[(i,d),v], but I can't get that to work :(
            
## This is as far as I need to go for now.
######################################################################################################
##
## Find the local maxima in the smoothed data. We want to make sure that we find maxima
## so we set the order to 10. This makes sure that the value returned is the maximum
## out of 10 points on either side.
#peaksUp = sig.argrelmax(-yfiltUp, order=Ord)
#peaksDn = sig.argrelmax(-yfiltDn, order=Ord)

## Adjust the data as necessary
## Make sure to take a look at the accelerating potentials for each peak to make
## sure they make sense. If necessary, increase "Ord", and only as a last resort
## should we delete elements of the peaks vector(s).
#a1u = [0] ## vector of indices to be deleted from the peaksUp and peaksDn results
#peaksUp = np.delete(peaksUp, a1u)
#a2u = [0,1,2,3,4,6,14]
#a2d = [0]
#peaksUp = np.delete(peaksUp, a2u)
#peaksDn = np.delete(peaksDn, a2d)
#a3u = [9]
#a3d = [0]
#peaksUp = np.delete(peaksUp, a3u)
#peaksDn = np.delete(peaksDn, a3d)
#a4u = [0]
#peaksUp = np.delete(peaksUp, a4u)

#print(xfiltUp[peaksUp])
#print(xfiltDn[peaksDn])

##################################
### Let's see what these data look like!
### Waveform first
#plt.figure(figsize=(12,6))
#plt.clf()
#plt.subplot(1,2,1)
#plt.plot(xfiltUp, -yfiltUp, 'b^', markersize=2, visible=True)
#plt.plot(xfiltDn, -yfiltDn, 'gv', markersize=2, visible=True)
#plt.plot(xfiltUp[peaksUp], -yfiltUp[peaksUp], 'bd', ls='none')
#plt.plot(xfiltDn[peaksDn], -yfiltDn[peaksDn], 'gd', ls='none')
## Give title to plot and axes, add a legend
#plt.xlabel(r'Accelerating Potential, $V_a$ ($V$)')
#plt.ylabel(r'Collector Current, $I_c$ ($\times 10^{-10}A$)')
#plt.title(r'Smoothed Franck-Hertz experiment results')
#plt.legend(handles=[pt1, pt2, pt3, pt4], loc=2, numpoints=5)
## Save the figure to disk
#plt.savefig(figName1)

### Then the peak potentials vs peak number
#plt.subplot(1,2,2)
#plt.plot(np.sort(xfiltUp[peaksUp]), 'b^')
#plt.plot(np.sort(xfiltDn[peaksDn]), 'gv')
#plt.xlim(-0.5,12.5)
#plt.ylim( 0.0,70.0)
#plt.xlabel(r'Peak Number')
#plt.ylabel(r'Accelerating Potential, $V_a$ ($V$)')
#plt.title(r'Accelerating potential as a function of peak number')
## Save the figure to disk
#plt.savefig(figName2)

## Close all plots
##plt.close('all')
