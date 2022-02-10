from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import uncertainties
from uncertainties import unumpy
from uncertainties import umath
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


def weightedSTD(values, weights):
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights)
    return (average, math.sqrt(variance))


#data = readCsv('intensity.csv',['Intensity','Density','Thickness'])
xUn = 0.0001

#137Cs with Pb
intensityCsPb = np.array(
    [512.78, 439.73, 433.76, 396.12, 376.9, 329.97, 312.89])
intUnCsPb = np.array([4.37, 3.36, 3.30, 2.63, 2.08, 2.57, 4.19])
intErrCsPb = unumpy.uarray(intensityCsPb, intUnCsPb)
xCsPb = np.array([0, 0.8, 0.9, 1.55, 2.13, 3.15, 4.05])
xCsPb = xCsPb/10
xErrCsPb = unumpy.uarray(xCsPb, xUn)
densityCsPb = 11.434
xCsPb = xCsPb * densityCsPb
poptCsPb, pcovCsPb = curve_fit(intensityFunc, xCsPb, intensityCsPb, [500, 0.1])
print(poptCsPb)
wAvg, wStd = weightedSTD(intensityCsPb, intUnCsPb)
#print(wAvg, wStd)
#extractMu = []
#for i in range(len(intErrCsPb)):
#    extractMu.append(-umath.log(intErrCsPb[i]
#                                / uncertainties.ufloat(495, 4.37))*densityCsPb/xErrCsPb[i])
#print(extractMu)
#print(np.average(unumpy.nominal_values(extractMu),
#      weights=unumpy.std_devs(extractMu)))
#137Cs with Al
xCsAl = np.array([0, 0.57, 0.6, 1.57, 2.55, 3.13, 5.03, 11.04])
xCsAl = xCsAl * 2.702 / 10
intensityCsAl = np.array(
        [512.78, 474.75, 467.25,  451.10, 440.50, 438.73, 417.85, 374.18])
intUnCsAl = np.array([4.37, 3.45, 2.3,  3.59, 4.18, 3.67, 3.13, 2.67])
poptCsAl, pcovCsAl = curve_fit(
            intensityFunc, xCsAl, intensityCsAl, [500, 0.075])
print(poptCsAl)

#60Co with Al
xCoAl = np.array([0, 0.4, 2.25, 3.13, 5.04,  7.29,  11.04]) * 2.702 / 10
intUnCoAl = np.array([0.89, 0.38, 0.21, 0.39, 0.74, 0.32, 1.1])
intUnCoAl2 = np.array([1.44, 0.68, 0.52, 0.16, 0.79, 1.12, 0.15])
intCoAl = np.array([45.40, 47.17, 43.99, 42.72, 42.53, 40.4, 39.96])
intCoAl2 = np.array([38.29, 39.25, 38.05, 36.87, 36.29, 34.63, 33.74])
poptCoAl, pcovCoAl = curve_fit(
            intensityFunc, xCoAl, intCoAl, [45, 0.05])
print(poptCoAl)
poptCoAl2, pcovCoAl2 = curve_fit(
          intensityFunc, xCoAl, intCoAl2, [45, 0.05])
print(poptCoAl2)
wAvg, wStd = weightedSTD(intCoAl, intUnCoAl)
print(wAvg, wStd)

#60Co with Pb
xCoPb = np.array([0, 0.83, 2.2, 6.45]) * 2.702 / 10
intUnCoPb = np.array([0.89, 0.67, 0.22, 0.13])
intUnCoPb2 = np.array([1.44, 0.91, 0.15, 0.55])
intCoPb = np.array([45.42, 44.71, 40.4, 30.93])
intCoPb2 = np.array([38.29, 37.91, 34.96, 27.01])
poptCoPb, pcovCoPb = curve_fit(
                    intensityFunc, xCoPb, intCoPb, [45, 0.05])
print(poptCoPb)
poptCoPb2, pcovCoPb2 = curve_fit(
                    intensityFunc, xCoPb, intCoPb2, [45, 0.05])
print(poptCoPb2)

# Edit these values
plotX = xCsPb
xUn = xUn
plotY = intensityCsPb
yUn = intUnCsPb
popt = poptCsPb
lab = 'I = '+str("%.3f" % popt[0])+'*e^(-'+str("%.3f" %
                                               popt[1])+'*x)'
fileName = 'CesiumPb.png'
title = "Cesium-137 with Lead Absorber"
# Stop editing values

yFunc = intensityFunc(plotX, *popt)
print(yFunc)

fig = plt.figure()
ax = fig.subplots()
ax.errorbar(plotX, plotY, xerr=xUn, yerr=yUn,
            fmt='ro', markersize=3, ecolor='black', capsize=2)
ax.errorbar(plotX, yFunc, fmt='r--', label=lab)
ax.set_xlabel('Density Thickness (g/cm^2)')
ax.set_ylabel('Intensity (counts per second)')
ax.set_title(title)
ax.legend()
'''
ax[1].errorbar(plotX, intCoPb2, xerr=xUn, yerr=intUnCoPb2,
               fmt='go', markersize=3, ecolor='black', capsize=2)
ax[1].errorbar(plotX, intensityFunc(plotX, *poptCoPb2), fmt='g--', label='I = '+str("%.3f" %
               poptCoPb2[0])+'*e^(-'+str("%.3f" % poptCoPb2[1])+'*x)')
ax[1].set_xlabel('Density Thickness (g/cm^2)')
ax[1].set_ylabel('Intensity (counts per second)')
ax[1].set_title("Cobalt-60 with Lead Absorber (1.173 MeV Emission)")
ax[1].legend()
'''
fig.set_dpi(300)
fig.tight_layout()
fig.savefig(fileName)
