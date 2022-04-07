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


def halfLife(t, a, b, c):
    return a*np.exp(-b*t)+c


createFig("Trial_1.spe", "Raw Timing Spectrum Trial 1", "trial1.png")
data1 = readSPE("Trial_1.spe")
data2 = readSPE("Trial_2.spe")
data3 = readSPE("Trial_3.spe")
data4 = readSPE("Adlab Complex Sean and Kevin Data.spe")
data5 = readSPE("2022_03_31_alpha_gamma_1800s.spe")
'''
for i in range(len(data1[0])):
    print(data1[1][i], data1[0][i], data2[0][i],
          data3[0][i], data4[0][i], data5[0][i])
'''
createFig("Trial_2.spe", "Trial 2", "trial2.png")
createFig("Trial_3.spe", "Trial 3", "trial3.png")
createFig("Adlab Complex Sean and Kevin Data.spe",
          "Raw Timing Spectrum Over 24 Hours", "overnight.png")
createFig("2022_03_31_alpha_gamma_1800s.spe",
          "Raw Timing Spectrum Over 30 Minutes", "short.png")
createFig("2022_03_31_alph_gam_cal_40ns_2p56us.Spe",
          'Timing Calibration Plot', "calibration.png")
data = readSPE("2022_03_31_alph_gam_cal_40ns_2p56us.spe")
bin = []
hit = []
for i in range(len(data[0])):
    if data[0][i] != 0:
        if len(bin) > 1:
            if data[1][i] - bin[-1] > 1:
                bin.append(data[1][i])
                hit.append(data[0][i])
        else:
            bin.append(data[1][i])
            hit.append(data[0][i])
avg = []
for i in range(len(bin)):
    if i == 0:
        continue
    else:
        avg.append(bin[i]-bin[i-1])
print(len(avg), len(hit))
hit.pop(0)
print(np.average(np.array(avg), weights=np.array(hit)))
time = 40/np.average(np.array(avg))
print(time)


fig = plt.figure(figsize=(9, 3))
ax = fig.subplots(1, 2)
ax[0].errorbar(data2[1], data2[0])
ax[0].set_title("Raw Timing Spectrum from Trial 1")
ax[0].set_ylabel('Counts')
ax[0].set_xlabel('Bin Number')
ax[1].errorbar(data3[1], data3[0])
ax[1].set_title("Raw Timing Spectrum from Trial 2")
ax[1].set_ylabel('Counts')
ax[1].set_xlabel('Bin Number')
plt.tight_layout()
fig.savefig("rawTimingSpecs.png")

data30Min = []
bin = []
hit = []
for i in range(len(data5[0])):
    if i > 600:
        if i < 851:
            bin.append(data5[1][i-600])
            hit.append(data5[0][i])
hit.reverse()
data30Min.append(hit)
data30Min.append(bin)
min30Popt, min30Pcov = curve_fit(halfLife, bin, hit, [35, 1/850, 0])
min30Un = np.sqrt(np.diag(min30Pcov))
print(len(bin))
print(min30Popt)
print(min30Un)
print(umath.log(2)
      / uncertainties.ufloat(min30Popt[1], min30Un[1])/time*10**(-9))
plus = min30Popt+min30Un
minus = min30Popt-min30Un
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(data30Min[1], data30Min[0])
ax.errorbar(bin, halfLife(np.array(bin), *min30Popt), label='I = '+str("%.3f" %
            min30Popt[0])+'*e^(-'+str("%.3f" % min30Popt[1])+'*x)+'+str("%.3f" % min30Popt[2]))
ax.errorbar(bin, halfLife(np.array(bin), *plus), fmt="k",label='Uncertainty due to the standard deviation of the parameters')
ax.errorbar(bin, halfLife(np.array(bin), *minus), fmt="k")

ax.set_ylabel('Counts')
ax.set_xlabel('Time (ns)')
ax.set_title('Measured Decay Over 30 Minutes')
ax.legend()
plt.tight_layout()
fig.savefig("specificData30Min.png")

data24Hr = []
bin = []
hit = []
for i in range(len(data4[0])):
    if i > 430:
        if i < 1000:
            bin.append(data4[1][i-430])
            hit.append(data4[0][i])
data24Hr.append(hit)
data24Hr.append(bin)
hr24Popt, hr24Pcov = curve_fit(halfLife, bin, hit, [1000, 1/1000, 0])
hr24Un = np.sqrt(np.diag(hr24Pcov))
plus = hr24Popt+hr24Un
minus = hr24Popt-hr24Un
print(len(bin))
print(hr24Popt)
print(plus)
print(minus)
print(hr24Un)
print(umath.log(2)/uncertainties.ufloat(hr24Popt[1], hr24Un[1])/time*10**(-9))
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(data24Hr[1], data24Hr[0])
ax.errorbar(bin, halfLife(np.array(bin), *hr24Popt), label='I = '+str("%.3f" %
            hr24Popt[0])+'*e^(-'+str("%.3f" % hr24Popt[1])+'*x)+'+str("%.3f" % hr24Popt[2]))
ax.errorbar(bin, halfLife(np.array(bin), *plus), fmt="k",label='Uncertainty due to the standard deviation of the parameters')
ax.errorbar(bin, halfLife(np.array(bin), *minus), fmt="k")
ax.set_ylabel('Counts')
ax.set_xlabel('Time (ns)')
ax.set_title('Measured Decay Over 24 Hours')
ax.legend()
plt.tight_layout()
fig.savefig("specificData24Hr.png")

dataTr2 = []
bin = []
hit = []
for i in range(len(data2[0])):
    if i > 100:
        if i < 330:
            bin.append(data2[1][i-100])
            hit.append(data2[0][i])
hit.reverse()
dataTr2.append(hit)
dataTr2.append(bin)
tr2Popt, tr2Pcov = curve_fit(halfLife, bin, hit, [350, 1/300, 0])
tr2Un = np.sqrt(np.diag(tr2Pcov))
print(tr2Popt)
print(tr2Un)
print(umath.log(2)/uncertainties.ufloat(tr2Popt[1], tr2Un[1])/time*10**(-9))
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(dataTr2[1], dataTr2[0])
ax.errorbar(bin, halfLife(np.array(bin), *tr2Popt), label='I = '+str("%.3f" %
            tr2Popt[0])+'*e^(-'+str("%.3f" % tr2Popt[1])+'*x)+'+str("%.3f" % tr2Popt[2]))
ax.set_ylabel('Counts')
ax.set_xlabel('Time (ns)')
ax.set_title('Measured Decay of Trial 1')
ax.legend()
plt.tight_layout()
fig.savefig("specificDataTr2.png")

dataTr3 = []
bin = []
hit = []
for i in range(len(data3[0])):
    if i > 100:
        if i < 330:
            bin.append(data3[1][i-100])
            hit.append(data3[0][i])
hit.reverse()
dataTr3.append(hit)
dataTr3.append(bin)
tr3Popt, tr3Pcov = curve_fit(halfLife, bin, hit, [350, 1/300, 0])
tr3Un = np.sqrt(np.diag(tr3Pcov))
print(tr3Popt)
print(tr3Un)
print(umath.log(2)/uncertainties.ufloat(tr3Popt[1], tr3Un[1])/time*10**(-9))
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(dataTr3[1], dataTr3[0])
ax.errorbar(bin, halfLife(np.array(bin), *tr3Popt), label='I = '+str("%.3f" %
            tr3Popt[0])+'*e^(-'+str("%.3f" % tr3Popt[1])+'*x)+'+str("%.3f" % tr3Popt[2]))
ax.legend()
ax.set_ylabel('Counts')
ax.set_xlabel('Time (ns)')
ax.set_title('Measured Decay of Trial 2')
plt.tight_layout()
fig.savefig("specificDataTr3.png")
