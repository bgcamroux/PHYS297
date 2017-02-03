# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:11:50 2017

@author: camroux
"""
import numpy as np
from scipy.optimize import curve_fit
from scipy import signal as sig


def funcLinear(x,m,b):
    """
    A linear function to use in the curve_fit routine, when necessary.    
    
    The independent variable MUST be sent first for the fit function.
    """
    return m*x+b
    
def funcExpon(x,a,b):
    """
    An exponential function to use in the curve-fit routine, when necessary.
    """
    return a*np.exp(b*x)

def funcWeightedFit(r, x, y, dx, dy):
    """
    Linear weighted fit of data.
    
    * r  = data frame containing (at a minimum) x, y, dx, and dy
    * x  = column of data frame to use for x-axis
    * y  = column of data frame to use for y-axis
    * dx = column of data frame to use for x-error
    * dy = column of data frame to use for y-error
    
    Each point is weighted by its uncertainty.
    
    """
    FitResults, Covariance = curve_fit(funcLinear, r[x], r[y], sigma=r[dy], absolute_sigma=True)
    FitUncert = np.sqrt(np.diag(Covariance))  ## Fit uncertainties (H&H equation 7.22)
    return FitResults, Covariance, FitUncert

def funcSmoothFilt(l, t, s, Data, r):
    """
    Use FFT Convolution with a gaussian to smooth data
    
    * winpar = [length, type, stdev], where length is the length of the window (this should be an ODD number), 
    type defines the type of window, and stdev is the standard deviation of the window
    * Data = data vector to be smoothed
    * r = rollback
    """
    window = sig.general_gaussian(l, t, s)
    filtered = sig.fftconvolve(window,Data)
    filtered = (np.average(Data)/np.average(filtered)) * filtered
    filtered = np.roll(filtered, r)
    return filtered

def funcResPrint(fit, dsname):
    """
    Print the results of the curve fitting to the screen.
    
    * fit = vector containing results from curve fitting routines : [*FitRes, *FitCovar, *FitUncert]
    * dsname = name of dataset
    """
    FitRes, FitCovar, FitUncert = fit
    # Print fit results to the console
    print('************ Fit Results: ', dsname, '************')
    print('Covariance matrix','\n', FitCovar)
    print('fit slope, slope uncertainty = ', FitRes[0], FitUncert[0])
    print('fit intercept, intercept uncertainty = ', FitRes[1], FitUncert[1])
    print('*************************************************\n\n')
    return
