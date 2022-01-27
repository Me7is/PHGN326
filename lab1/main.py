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

n = 1

def linFitStep10(bin,a,b):
    return a * bin - b

def fitStep12(r,a,b,c):
    return a/((r+b)**3)+c

binData = readCsv('binVsEnergyData.csv',['Bin Number','Uncertainty','Energy (KeV)'])
bin = unumpy.uarray(binData[0],binData[1])
energy = unumpy.uarray(binData[2],np.zeros(len(binData[2])))

distanceData = readCsv('rSquaredData.csv',['Distance from detector (cm)','Distance uncertainty','Counts per second','Uncertainty'])
distance = unumpy.uarray(distanceData[0],distanceData[1])
countsPerSec = unumpy.uarray(distanceData[2],distanceData[3])

print(np.size(unumpy.nominal_values(bin)))
print(np.size(unumpy.nominal_values(energy)))
print(np.size(unumpy.nominal_values(distance)))
print(np.size(unumpy.nominal_values(countsPerSec)))

energyPopt,energyPcov = curve_fit(linFitStep10,unumpy.nominal_values(bin),unumpy.nominal_values(energy))

rPopt,rPcov = curve_fit(fitStep12,unumpy.nominal_values(distance),unumpy.nominal_values(countsPerSec))

plt.plot(unumpy.nominal_values(distance),fitStep12(unumpy.nominal_values(distance),*rPopt),'g--')
plt.savefig('test.png')
