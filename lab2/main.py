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

def intensityFunc(distance,i0,mu):
    return i0*np.exp(-mu*distance)

def weightedSTD(values,weights):
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights)
    return (average, math.sqrt(variance))

#data = readCsv('intensity.csv',['Intensity','Density','Thickness'])
xUn = 0.0001

intensityCsPb = np.array([512.78,439.73,312.89,433.76,376.9,329.97,396.12])
intUnCsPb = np.array([4.37,4.01,5.54,6.91,6.24,5.89,6.42])
xCsPb = np.array([0,0.8,4.05,0.9,2.13,3.15,1.55])
xCsPb = xCsPb/10
densityCsPb = 11.434
xCsPb = xCsPb * densityCsPb
poptCsPb,pcovCsPb = curve_fit(intensityFunc,x,intensity,[500,0.1])
print(poptCsPb)
wAvg,wStd = weightedSTD(intensityCsPb,intUnCsPb)
print(wAvg,wStd)

xCsAl = np.array([0,0.6,0.57,1.57,2.55,3.13,5.03,11.04])
xCsAl = xCsAl * 2.702 / 10
intensityCsAl = np.array([512.78,467.25,474.75,451.10,440.50,438.73,417.85,374.18])
poptCsAl,pcovCsAl = curve_fit(intensityFunc,xAl,intensityAl,[500,0.075])
print(popt)

xCoAl = np.array([0,3.13,5.04,2.25,7.29,0.4,11.04]) * 2.702 / 10
intUn = np.array([1.5,1.45,1.4,1.46,1.38,1.54,1.32])
intCoAl = np.array([45.42,42.73,42.55,43.99,39.88,47.18,40.0])
poptCoAl,pcovCoAl = curve_fit(intensityFunc,xCoAl,intCoAl,[45,0.05])
print(popt)
wAvg,wStd = weightedSTD(intCoAl,intUn)
print(wAvg,wStd)

xCoPb = np.array([0,0.83,2.2,6.45]) * 2.702 / 10
#intUnCoPb = np.array([1.5,1.45,,1.78])
intCoPB = np.array([45.42,44.71,40.4,30.93])
poptCoPb,pcovCoPb = curve_fit(intensityFunc,xCoAl,intCoAl,[45,0.05])
print(popt)

# Edit these values
plotX = xCoPb
xUn = xUn
plotY = intCoPB
yUn = intUnCoPb
popt = poptCoPb
fileName = 'CobaltAltest.png'
# Stop editing values

yFunc = intensityFunc(plotX,*popt)

fig = plt.figure()
ax = fig.subplots(1,1)
ax.errorbar(plotX,plotY,xerr = xUn,yerr = yUn,fmt = 'ro')
ax.errorbar(plotX,yFunc,fmt='r--')
ax.set_xlabel('Density Thickness')
ax.set_ylabel('Intensity')
fig.set_dpi(300)
fig.tight_layout()
fig.savefig(fileName)
