from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import uncertainties
from uncertainties import unumpy
from uncertainties import umath
import math
import pandas as pd
import datetime


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


def createFig(importName, title, exportName):
    data = readSPE(importName)
    fig = plt.figure()
    ax = fig.subplots()
    ax.errorbar(data[1], data[0])
    ax.set_title(title)
    ax.set_ylabel('Counts')
    ax.set_xlabel('Bin Number')
    plt.tight_layout()
    fig.savefig(exportName)


def stability(t, a, b):
    return a*t+b


createFig("Na 22 Spectra/detect1/Na 22 2min Spectrum Detector 1 Gated.Spe",
          'Detector 1 Gated Spectrum', 'detect1GateSpec.png')
createFig("Na 22 Spectra/detect1/Na 22 5min Spectrum Detector 1 Ungated.Spe",
          'Detector 1 Ungated Spectrum', 'detect1NogateSpec.png')
createFig("Na 22 Spectra/Detector 2/Na 22 2min Spectrum Detector 2 Gated.Spe",
          'Detector 2 Gated Spectrum', 'detect2GateSpec.png')
createFig("Na 22 Spectra/Detector 2/Na 22 5min Spectrum Detector 2 Ungated.Spe",
          'Detector 2 Ungated Spectrum', 'detect2NogateSpec.png')
detect2Gate = readSPE(
    "Na 22 Spectra/Detector 2/Na 22 2min Spectrum Detector 2 Gated.Spe")
print(detect2Gate[0].index(max(detect2Gate[0])))
print(detect2Gate[1][448])
print(detect2Gate[0][448])
calibEn1 = np.array([511, 662, 1274, 1460])
calibBin1 = np.array([445.79, 571.22, 1090.77, 1249.44])
calibEn2 = np.array([511, 662, 1274, 1460])
calibBin2 = np.array([445.13, 571.03, 1081.95, 1237.79])
calibLine = np.linspace(0, 2048)
calibPopt1, calibPcov1 = curve_fit(stability, calibBin1, calibEn1)
calibPopt2, calibPcov2 = curve_fit(stability, calibBin2, calibEn2)
print(np.sqrt(np.diag(calibPcov1)))
print(np.sqrt(np.diag(calibPcov2)))

for i in range(len(detect2Gate[1])):
    print(detect2Gate[1][i], detect2Gate[0][i])
i = 0
sum = 0
while i < 387:
    sum += detect2Gate[0][i]
    i += 1
i = 387
sum2 = 0
while i < 500:
    sum2 += detect2Gate[0][i]
    i += 1
print(sum, sum2)
#print(np.sqrt(np.diag(calibPcov)))
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(calibLine, stability(np.array(calibLine), *calibPopt1),
            fmt='g--', label='Energy = '+str("%.3f" % calibPopt1[0])+' * Bin + '+str("%.3f" % calibPopt1[1]))
ax.errorbar(calibBin1, calibEn1,
            fmt='ro', markersize=3, ecolor='black', capsize=2,)
ax.set_xlabel('Bin Number')
ax.set_ylabel('Energy (keV)')
ax.set_title('Detector 1 Calibration Plot')
ax.legend()
fig.set_dpi(300)
fig.tight_layout()
fig.savefig('calibrationDetect1.png')
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(calibLine, stability(np.array(calibLine), *calibPopt2),
            fmt='g--', label='Energy = '+str("%.3f" % calibPopt2[0])+' * Bin + '+str("%.3f" % calibPopt2[1]))
ax.errorbar(calibBin2, calibEn2,
            fmt='ro', markersize=3, ecolor='black', capsize=2,)
ax.set_xlabel('Bin Number')
ax.set_ylabel('Energy (keV)')
ax.set_title('Detector 2 Calibration Plot')
ax.legend()
fig.set_dpi(300)
fig.tight_layout()
fig.savefig('calibrationDetect2.png')

chi1 = np.sum(np.power(calibEn1 - stability(calibBin1, *calibPopt1),
              2)/stability(calibBin1, *calibPopt1))
chi2 = np.sum(np.power(calibEn2 - stability(calibBin2, *calibPopt2),
              2)/stability(calibBin2, *calibPopt2))

print(chi1, chi2)
