# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:41:56 2017

Develop a calibration curve by analyzing the instrument calibration data.

Note that the collector current data and uncertainties are each 10 orders of magnitude
smaller than the physical values.

@author: brad
"""

import os

if os.getlogin()=='brad':
    os.chdir('/home/brad/Documents/UAlberta/W17/PHYS297/Franck-Hertz/Analysis/')
elif os.getlogin()=='camroux':
    os.chdir('/home/')
else:
    os.chdir('/home/')

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd   ## PANDAS is glorious and makes handling data easier, much like in R!
import BGCprocLib as bgc ## These are functions built to make processing quicker or easier

## Read the CSV data file into a data frame using PANDAS
fname = '../Data/00_FranckHertz_InstCalib_23Jan2017_Camroux-Rocha.csv'
calData = pd.read_csv(fname, sep=',')
### File consists of eight columns and 11 records
###    Col A: Va       - Accelerating potential (V) as read from power supply display
###    Col B: dVa      - Uncertainty in accelerating potential (V) (limit uncertainty, last digit of display)
###    Col C: CH1_Pot  - LabPro Channel 1 potential (V), proportional to accelerating potential
###    Col D: dCH1_Pot - Uncertainty in LabPro Channel 1 potential (V)
###    Col E: I        - Collector current (e-10 A) as read from electrometer
###    Col F: dI       - Uncertainty in collector current (e-10 A) (variation in needle position around central value)
###    Col G: CH2_Pot  - LabPro Channel 2 potential (V), proportional to collector current
###    Col H: dCH2_Pot - Uncertainty in LabPro Channel 2 potential (V)
###################################

## Column names for least squares fitting routine
y1, dy1  = ['Va', 'dVa']            ## x-axis variable & its error
x1, dx1  = ['CH1_Pot', 'dCH1_Pot']  ## y-axis variable & its error
y2, dy2  = ['I', 'dI']              ## x-axis variable & its error
x2, dx2  = ['CH2_Pot', 'dCH2_Pot']  ## y-axis variable & its error

## Calculate least-squares fit for accelerating voltage and collector current data sets
VaFitRes, VaFitCovar, VaFitUncert = bgc.funcWeightedFit(calData, x1, y1, dx1, dy1)
IcFitRes, IcFitCovar, IcFitUncert = bgc.funcWeightedFit(calData, x2, y2, dx2, dy2)

bgc.funcResPrint([VaFitRes, VaFitCovar, VaFitUncert], 'Accelerating Voltage')
bgc.funcResPrint([IcFitRes, IcFitCovar, IcFitUncert], 'Collector Current')

###############################
xVa = np.arange(-3,1)   ## Range for plotting calibration curves
xIc = np.arange(0,3,0.25)  ## Range for plotting calibration curves

plt.figure()
plt.clf()
plt.hold(True) # hold on to include the fits
plt.errorbar(calData[x1], calData[y1], xerr=calData[dx1], yerr=calData[dy1], fmt='o', ls='none', markersize=4, color='black')
plt.plot(xVa,bgc.funcLinear(xVa,VaFitRes[0],VaFitRes[1]),'g-')
plt.xlim(-3,0.)
plt.xlabel(r'Channel 1 Potential (V)')
plt.ylabel(r'Accelerating Potential, $V_a$ (V)')
plt.title(r'Calibration of Accelerating Potential for LabPro Data')
plt.hold(False)
#
plt.figure()
plt.clf()
plt.hold(True)
plt.errorbar(calData[x2], calData[y2], xerr=calData[dx2], yerr=calData[dy2], fmt='o', ls='none', markersize=4, color='black')
plt.plot(xIc,bgc.funcLinear(xIc,IcFitRes[0],IcFitRes[1]),'b-')
plt.xlim(0,2.5)
plt.xlabel(r'Channel 2 Potential (V)')
plt.ylabel(r'Collector Current, $I_c$ ($\times 10^{-10}$ A)')
plt.title(r'Calibration of Collector Current for LabPro Data')
plt.hold(False)