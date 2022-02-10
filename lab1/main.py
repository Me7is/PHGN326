from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import uncertainties
from uncertainties import unumpy
import math
import pandas as pd

# Format data to be plotted


def CreateErrorBar(x, y, xerr=None, yerr=None, fmt=None, ecolor=None, elinewidth=None, capsize=None, capthick=None, barsabove=False, label=None):
    return[x, y, xerr, yerr, fmt, ecolor, elinewidth, capsize, capthick, barsabove, label]

# Plot formatted data


def CreatePlot(dataNum, data, xLabel, yLabel, Title, fileName):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    legendBool = False
    for i in range(dataNum):
        ax.errorbar(data[i][0], data[i][1], xerr=data[i][2], yerr=data[i][3], label=data[i][10], fmt=data[i][4],
                    ecolor=data[i][5], elinewidth=data[i][6], capsize=data[i][7], capthick=data[i][8], barsabove=data[i][9])
        if data[i][10]:
            legendBool = True
    ax.set_title(Title)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    if legendBool:
        ax.legend()
    fig.set_dpi(300)
    fig.savefig(fileName)


def readCsv(fileName, labels):
    data1 = pd.read_csv(fileName)
    dataList1 = []
    for i in labels:
        dataList1.append(data1[i].tolist())
    return dataList1


def readSPE(fileName):
    with open(fileName) as inspec:
        _hit1 = []
        for line in inspec:
            if not "0 2047\n" in line:
                continue
            for line in inspec:
                if "$ROI:\n" in line:
                    break
                _hit1.append(np.int(line))
        _bin1 = list(range(0, len(_hit1)))

    return [_hit1, _bin1]


def linFitStep10(bin, a, b):
    return a * bin - b


def fitStep12(r, a, b):
    return a/(r**2) + b


def fitStep12Lin(r, a, b, c):
    return a/((r+b)**1)+c


def fitStep12Square(r, a, b, c):
    return a/((r+b)**2)+c


def fitStep12Cube(r, a, b, c):
    return a/((r+b)**3)+c


backgroundSpec = readSPE('Background Energy Spectra 20cm 10min.Spe')
Co60Spec = readSPE('Co60 Energy Spectra 20cm 10min.Spe')
differenceCo = [np.array(Co60Spec[0])
                - np.array(backgroundSpec[0]), backgroundSpec[1]]
Cs137Spec = readSPE('Cs137 Energy Spectra 20cm 10min.Spe')
differenceCs = [np.array(Cs137Spec[0])
                - np.array(backgroundSpec[0]), backgroundSpec[1]]

binData = readCsv('binVsEnergyData.csv', [
                  'Bin Number', 'Uncertainty', 'Energy (KeV)'])
bin = unumpy.uarray(binData[0], binData[1])
energy = unumpy.uarray(binData[2], np.zeros(len(binData[2])))

distanceData = readCsv('rSquaredData.csv', [
                       'Distance from detector (cm)', 'Distance uncertainty', 'Counts per second', 'Uncertainty'])
distance = unumpy.uarray(distanceData[0], distanceData[1])
countsPerSec = unumpy.uarray(distanceData[2], distanceData[3])

energyPopt, energyPcov = curve_fit(
    linFitStep10, unumpy.nominal_values(bin), unumpy.nominal_values(energy))

print(np.sum(np.power(unumpy.nominal_values(energy)
                      - linFitStep10(unumpy.nominal_values(bin), *energyPopt), 2)/unumpy.nominal_values(energy)))
rPopt, rPcov = curve_fit(fitStep12, unumpy.nominal_values(
    distance), unumpy.nominal_values(countsPerSec))

rLinPopt, rLinPcov = curve_fit(fitStep12Lin, unumpy.nominal_values(
    distance), unumpy.nominal_values(countsPerSec))

rSquarePopt, rSquarePcov = curve_fit(fitStep12Square, unumpy.nominal_values(
    distance), unumpy.nominal_values(countsPerSec), rLinPopt)
rCubePopt, rCubePcov = curve_fit(fitStep12Cube, unumpy.nominal_values(
    distance), unumpy.nominal_values(countsPerSec), rLinPopt)
chi2 = np.sum(np.power(unumpy.nominal_values(countsPerSec)
                       - fitStep12(unumpy.nominal_values(distance), *rPopt), 2)/unumpy.nominal_values(countsPerSec))
print(chi2)
linChi2 = np.sum(np.power(unumpy.nominal_values(countsPerSec)
                 - fitStep12Lin(unumpy.nominal_values(distance), *rLinPopt), 2)/unumpy.nominal_values(countsPerSec))
print(linChi2)
squareChi2 = np.sum(np.power(unumpy.nominal_values(countsPerSec)
                             - fitStep12Square(unumpy.nominal_values(distance), *rSquarePopt), 2)/unumpy.nominal_values(countsPerSec))
print(squareChi2)
cubeChi2 = np.sum(np.power(unumpy.nominal_values(countsPerSec)
                           - fitStep12Cube(unumpy.nominal_values(distance), *rCubePopt), 2)/unumpy.nominal_values(countsPerSec))
print(cubeChi2)

fontDict = {'fontsize': 15}
fig = plt.figure(figsize=(7, 9))
ax = fig.subplots(3, 1)
ax[0].errorbar(backgroundSpec[1], backgroundSpec[0])
ax[0].set_title('Background Radiation', fontdict=fontDict)
ax[0].set_ylabel('Counts')
ax[0].set_xlabel('Bin Number')
ax[1].errorbar(Co60Spec[1], Co60Spec[0])
ax[1].set_title('Co-60 with Background Radiation', fontdict=fontDict)
ax[1].set_ylabel('Counts')
ax[1].set_xlabel('Bin Number')
ax[2].errorbar(differenceCo[1], differenceCo[0])
ax[2].set_title('Co-60 Minus Background Radiation', fontdict=fontDict)
ax[2].set_xlabel('Bin Number')
ax[2].set_ylabel('Counts')
plt.tight_layout()
fig.savefig('coPlots.png')

fig = plt.figure(figsize=(7, 9))
ax = fig.subplots(3, 1)
ax[0].errorbar(backgroundSpec[1], backgroundSpec[0])
ax[0].set_title('Backgorund Radiation', fontdict=fontDict)
ax[0].set_ylabel('Counts')
ax[0].set_xlabel('Bin Number')
ax[1].errorbar(Cs137Spec[1], Cs137Spec[0])
ax[1].set_title('Cs-137 with Background Radiation', fontdict=fontDict)
ax[1].set_ylabel('Counts')
ax[1].set_xlabel('Bin Number')
ax[2].errorbar(differenceCs[1], differenceCs[0])
ax[2].set_title('Cs-137 Minus Background Radiation', fontdict=fontDict)
ax[2].set_xlabel('Bin Number')
ax[2].set_ylabel('Counts')
plt.tight_layout()
fig.savefig('csPlots.png')

fig = plt.figure(figsize=(7, 9))
ax = fig.subplots(3, 1)
ax[0].errorbar(backgroundSpec[1], backgroundSpec[0])
ax[0].set_title('Backgorund Radiation', fontdict=fontDict)
ax[0].set_ylabel('Counts')
ax[0].set_xlabel('Bin Number')
ax[1].errorbar(Co60Spec[1], Co60Spec[0])
ax[1].set_title('Co-60 with Background Radiation', fontdict=fontDict)
ax[1].set_ylabel('Counts')
ax[1].set_xlabel('Bin Number')
ax[2].errorbar(Cs137Spec[1], Cs137Spec[0])
ax[2].set_title('Cs-137 with Background Radiation', fontdict=fontDict)
ax[2].set_xlabel('Bin Number')
ax[2].set_ylabel('Counts')
plt.tight_layout()
fig.savefig('AllRadPlots.png')
print(energyPopt)
fig = plt.figure()
ax = fig.subplots(1, 1)
ax.errorbar(unumpy.nominal_values(bin), unumpy.nominal_values(
    energy), xerr=unumpy.std_devs(bin), fmt='bo')
ax.errorbar(unumpy.nominal_values(
    bin), linFitStep10(unumpy.nominal_values(bin), *energyPopt), fmt='b--', label='f(bin) = '+str("%.2f" % energyPopt[0])+'*bin-'+str("%.2f" % energyPopt[1]))
ax.set_title('Energy vs Bin Number')
ax.set_xlabel('Bin')
ax.set_ylabel('Gamma Ray Emission Energy (KeV)')
ax.legend()
fig.set_dpi(300)
fig.savefig('binEnergy.png')

fig = plt.figure(figsize=(7, 10))
ax = fig.subplots(4, 1)
ax[0].errorbar(unumpy.nominal_values(distance), unumpy.nominal_values(
    countsPerSec), xerr=unumpy.std_devs(distance), yerr=unumpy.std_devs(countsPerSec), fmt='ko', ecolor='black')
ax[0].errorbar(unumpy.nominal_values(distance), fitStep12(
    unumpy.nominal_values(distance), *rPopt), fmt='m--', label='f(r) = '+str("%.2f" % rPopt[0])+'/(r^2)+'+str("%.2f" % rPopt[1]))
ax[0].set_title('Orthogonal Distance Regression')
ax[0].set_xlabel('Distance from detector (cm)')
ax[0].set_ylabel('Counts per Second')
ax[0].legend()
ax[1].errorbar(unumpy.nominal_values(distance), unumpy.nominal_values(
    countsPerSec), xerr=unumpy.std_devs(distance), yerr=unumpy.std_devs(countsPerSec), fmt='ko', ecolor='black')
ax[1].errorbar(unumpy.nominal_values(distance), fitStep12Lin(
    unumpy.nominal_values(distance), *rLinPopt), fmt='r--', label='f(r) = '+str("%.2f" % rLinPopt[0])+'/(r+'+str("%.2f" % rLinPopt[1])+')+'+str("%.2f" % rLinPopt[2]))
ax[1].set_xlabel('Distance from detector (cm)')
ax[1].set_ylabel('Counts per Second')
ax[1].legend()
ax[2].errorbar(unumpy.nominal_values(distance), unumpy.nominal_values(
    countsPerSec), xerr=unumpy.std_devs(distance), yerr=unumpy.std_devs(countsPerSec), fmt='ko', ecolor='black')
ax[2].errorbar(unumpy.nominal_values(distance), fitStep12Square(
    unumpy.nominal_values(distance), *rSquarePopt), fmt='g--', label='f(r) = '+str("%.2f" % rSquarePopt[0])+'/(r+'+str("%.2f" % rSquarePopt[1])+')^2+'+str("%.2f" % rSquarePopt[2]))
ax[2].set_xlabel('Distance from detector (cm)')
ax[2].set_ylabel('Counts per Second')
ax[2].legend()
ax[3].errorbar(unumpy.nominal_values(distance), unumpy.nominal_values(
    countsPerSec), xerr=unumpy.std_devs(distance), yerr=unumpy.std_devs(countsPerSec), fmt='ko', ecolor='black')
ax[3].errorbar(unumpy.nominal_values(distance), fitStep12Cube(
    unumpy.nominal_values(distance), *rCubePopt), fmt='b--', label='f(r) = '+str("%.2f" % rCubePopt[0])+'/(r+'+str("%.2f" % rCubePopt[1])+')^3+'+str("%.2f" % rCubePopt[2]))
ax[3].set_xlabel('Distance from detector (cm)')
ax[3].set_ylabel('Counts per Second')
ax[3].legend()
fig.set_dpi(300)
plt.tight_layout()
fig.savefig('rTest.png')


#plt.plot(unumpy.nominal_values(distance), fitStep12Lin(unumpy.nominal_values(distance), *rLinPopt), 'g--')
