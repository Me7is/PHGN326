from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import uncertainties
from uncertainties import unumpy
import math
import pandas as pd


def readCsv(fileName, labels):
    data1 = pd.read_csv(fileName)
    dataList1 = []
    for i in labels:
        dataList1.append(data1[i].tolist())
    return dataList1


def intensityFunc(distance, i0, mu):
    return i0*np.exp(-mu*distance)

#data = readCsv('intensity.csv',['Intensity','Density','Thickness'])


#137Cs with Pb
intensity = np.array([512.78, 439.73, 312.89, 433.76, 376.9, 329.97, 396.12])
x = np.array([0, 0.8, 4.05, 0.9, 2.13, 3.15, 1.55])
x = x/10
density = 11.434
x = x * density
print(x)

popt, pcov = curve_fit(intensityFunc, x, intensity, [500, 0.1])
print(popt)

#137Cs with Al
xAl = np.array([0, 0.6, 0.57, 1.57, 2.55, 3.13, 5.03])
xAl = xAl * 2.702 / 10
intensityAl = np.array(
    [512.78, 467.25, 474.75, 451.10, 440.50, 438.73, 417.85])
popt, pcov = curve_fit(intensityFunc, xAl, intensityAl, [500, 0.1])
print(popt)

#60Co with Al
xLin = np.linspace(0, 20, num=50)
xCoAl = np.array([0, 3.13, 5.04, 2.25, 7.29, 0.4]) * 2.702 / 10
intCoAl = np.array([45.42, 42.73, 42.55, 43.99, 39.88, 47.18])
popt, pcov = curve_fit(intensityFunc, xCoAl, intCoAl, [45, 0.05])
print(popt)




fig = plt.figure()
ax = fig.subplots(1, 1)
ax.errorbar(xCoAl, intCoAl, fmt='ro')
ax.errorbar(xLin, intensityFunc(xLin, *popt), fmt='r--')
ax.set_xlabel('Density Thickness')
ax.set_ylabel('Intensity')
fig.savefig('CobaltAltest.png')
