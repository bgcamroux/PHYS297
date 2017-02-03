# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 21:54:58 2017

@author: brad
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd   ## PANDAS is glorious and makes handling data easier, much like in R!
#from scipy import stats
#from scipy import signal as sig

import BGCprocLib as bgc

peakFile = '../Data/05_FranckHertz_Peaks-and-Temps_01Feb2017.csv'
PeakTempIndex = pd.read_csv(peakFile, sep=',', header=0, index_col=[0,1])
## Data file format:
##    Col 0: temp      - temperature at which experiment was performed
##    Col 1: direction - increasing or decreasing accelerating potential
##                           0: decreasing
##                           1: increasing
##    Col 2: index     - peak number, starting from 1
##    Col 3: potential - value of accelerating potential for peak at the corresponding
##                       temperature, direction, and index.

#######
## Let's plot the peaks vs. peak number to get at the excitation energy.
## One plot per temperature, but we'll put both increasing and decreasing potentials on each
temps = [152,161,172,178,180,190]
col = ['r', 'g', 'b', 'c', 'm', 'k']
for i in temps:
    x = PeakTempIndex.loc[i]['index']       ## peak indices for corresponding temperature
    y = PeakTempIndex.loc[i]['potential']   ## peak potentials for corresponding temperature
    rge = np.arange(0,15)                   ## range of x values for linear fit plotting

    ## Do a least squares regression
    FitResults, Covariance = curve_fit(bgc.funcLinear, x, y, absolute_sigma=False)
    FitUncert = np.sqrt(np.diag(Covariance))  ## Fit uncertainties (H&H equation 7.22)
    ## Print the best fit results to the console.
    #bgc.funcResPrint([FitResults, Covariance, FitUncert], i)
 
    plt.figure(i, figsize=(8,10))
    plt.clf()
    plt.hold(True)       ## Hold the plots so we can put a couple things on there (points and line fit)
    plt.plot(rge, bgc.funcLinear(rge, FitResults[0], FitResults[1])) ## Plot the linear fit first
    ## We want to plot increasing and decreasing potentials separately, using different symbols, so we
    ## will split them here using a FOR loop
    for d in [0,1]:
        if d==0:         ## Decreasing potentials
            mkr = 'v'    ## plot symbol
            vis = True   ## should we display this set?
        elif d==1:       ## Increasing potentials
            mkr = '^'    ## plot symbol
            vis = True   ## should we display this set?
        ## Now plot the data
        plt.plot(PeakTempIndex.loc[i].loc[d]['index'], PeakTempIndex.loc[i].loc[d]['potential'], marker=mkr, ls='none', visible=vis)
    plt.hold(False)   ## Release the plot
    textstr1 = '$\mathrm{Temperature}=%i \,\degree{C}$ \n$\mathrm{Slope}=%0.3f\pm%0.3f$ \n$y\mathrm{-intercept}=%0.1f\pm%0.1f$'%(i, FitResults[0], FitUncert[0], FitResults[1], FitUncert[1])    
    
    ## Add some annotation to help with the interpretation of the plot
    textxpos, textypos = (2, 60)   ## position of annotation (in data units)
    plt.text(textxpos, textypos, textstr1, fontsize = 10)
    plt.xlabel(r'Peak Number')
    plt.ylabel(r'Accelerating Potential, $V_a$ ($V$)')
    plt.xlim(0,14)
    plt.ylim(0,80)
    imagename = '../Figures/02_FranckHertz_PeaksVsIndex_Temp-' + str(i) + '.eps'
    plt.savefig(imagename)
#plt.legend(line_152, line_161, line_172, line_178, line_180, line_190)