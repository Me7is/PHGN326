from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import uncertainties
from uncertainties import unumpy
from uncertainties import umath
import math
import pandas as pd
import datetime
'''
with open('Spec000.Rpt', 'r') as file:
    data = file.readlines()
    for i in range(len(data)):
        print(i, ':', data[i])
        word = data[i].split()
        for j in range(len(word)):
            print(i, j, ":", word[j])
'''


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


def saveSPE(type):
    hit = []
    bin = []
    for k in range(type[2]):
        if k < 10:
            location = type[0]+'Spec'+'00'+str(k)+'.Spe'
        else:
            location = type[0]+'Spec'+'0'+str(k)+'.Spe'
        spe = readSPE(location)
        hit.append(spe[0])
        bin.append(spe[1])
    return [hit, bin]


def parseReport(filename, peakNum):
    words = []
    with open(filename, 'r') as file:
        data = file.readlines()
        for i in range(len(data)):
            words.append(data[i].split())
    time = words[1][5].split(':')
    date = datetime.datetime(2022, 2, 17, hour=int(
        time[0]), minute=int(time[1]), second=int(time[2]))
    roi = (peakNum * 7) - 2
    count = uncertainties.ufloat(int(words[roi+1][7]), int(words[roi+1][9]))
    center = float(words[roi+2][1])
    return [date, count, center]


def saveRpt(type):
    data = []
    time = []
    center = []
    for i in range(len(type[1])):
        temp = []
        tempTime = []
        tempUncertainty = []
        tempCenter = []
        t0 = 0
        for k in range(type[2]):
            if k < 10:
                location = type[0]+'Spec'+'00'+str(k)+'.Rpt'
            else:
                location = type[0]+'Spec'+'0'+str(k)+'.Rpt'

            parse = parseReport(location, type[1][i])
            if k == 0:
                t0 = parse[0]
            temp.append(parse[1].nominal_value)
            tempTime.append((parse[0]-t0).seconds)
            tempUncertainty.append(parse[1].std_dev)
            tempCenter.append(parse[2])
            tempVal = unumpy.uarray(temp, tempUncertainty)
        data.append(tempVal)
        time.append(tempTime)
        center.append(tempCenter)
    return data, time, type, center


def getPopt(data, time, type):
    popt = []
    pcov = []
    for i in range(len(data[2][1])):
        tempPopt, tempPcov = curve_fit(
            halfLife, time[i], unumpy.nominal_values(data[i]), type[3][i])
        popt.append(tempPopt)
        pcov.append(tempPcov)
    return popt, pcov


def halfLife(t, a, b, c):
    return a*np.exp(-b*t)+c


def stability(t, a, b):
    return a*t+b


mg = ['Mg27/', [1, 2], 15, [[5000, 0.001, 0], [5000, 0.001, 0]],
      ['Mg-27 844 keV Decay', 'Mg-27 1.014 MeV Decay']]
na = ['Na24/', [3, 5], 6,
      [[13000, 1.29*10**(-5), 0], [7000, 1.29*10**(-5), 0]], ['Na-24 1.368 MeV Decay', 'Na-24 2.754 MeV Decay']]
al = ['Al28/', [4], 30, [[2000, 0.005, 0]], ['Al-28 1.779 MeV Decay']]
cs = ['Cs137 Stability Test 10x1.5m/', [1], 10,
      [-0.07, 400], ['Cs-137 Stability Test']]

mgData, mgTime, mg, mgCent = saveRpt(mg)
naData, naTime, na, naCent = saveRpt(na)
alData, alTime, al, alCent = saveRpt(al)
mgSpe = saveSPE(mg)
naSpe = saveSPE(na)
alSpe = saveSPE(al)
fig = plt.figure(figsize=(20, 9))
ax = fig.subplots(3, 5)
for i in range(3):
    for j in range(5):
        num = i*5+j
        print(num)
        if num < 10:
            title = 'Mg-27 Spec00'+str(num)
        else:
            title = 'Mg-27 Spec0'+str(num)
        ax[i][j].errorbar(mgSpe[1][num], mgSpe[0][num])
        ax[i][j].set_title(title)
        ax[i][j].set_ylabel('Counts')
        ax[i][j].set_xlabel('Bin Number')
plt.tight_layout()
fig.savefig('mgRaw.png')

fig = plt.figure(figsize=(12, 6))
ax = fig.subplots(2, 3)
for i in range(2):
    for j in range(3):
        num = i*3+j
        print(num)
        if num < 10:
            title = 'Na-24 Spec00'+str(num)
        else:
            title = 'Na-24 Spec0'+str(num)
        ax[i][j].errorbar(naSpe[1][num], naSpe[0][num])
        ax[i][j].set_title(title)
        ax[i][j].set_ylabel('Counts')
        ax[i][j].set_xlabel('Bin Number')
plt.tight_layout()
fig.savefig('naRaw.png')

fig = plt.figure(figsize=(24, 15))
ax = fig.subplots(5, 6)
for i in range(5):
    for j in range(6):
        num = i*6+j
        print(num)
        if num < 10:
            title = 'Al-28 Spec00'+str(num)
        else:
            title = 'Al-28 Spec0'+str(num)
        ax[i][j].errorbar(alSpe[1][num], alSpe[0][num])
        ax[i][j].set_title(title)
        ax[i][j].set_ylabel('Counts')
        ax[i][j].set_xlabel('Bin Number')
plt.tight_layout()
fig.savefig('alRaw.png')

csData, csTime, cs, csCent = saveRpt(cs)
csX = np.linspace(1, len(csCent[0]), num=10)
csPopt, csPcov = curve_fit(stability, csX, np.array(csCent[0]))
poptUp = np.array(csPopt) + np.sqrt(np.diag(csPcov))
poptDown = np.array(csPopt) - np.sqrt(np.diag(csPcov))
lab = 'Bin = '+str("%.3f" % csPopt[0])+' * x + '+str("%.3f" % csPopt[1])
fig = plt.figure()
ax = fig.subplots()
#ax.errorbar(csX, stability(np.array(csX), *poptUp), fmt='k-',
#            label='Uncertainty due to the standard deviation of the parameters')
#ax.errorbar(csX, stability(np.array(csX), *poptDown), fmt='k-')
ax.errorbar(csX, stability(np.array(csX), *csPopt),
            fmt='g--', label=lab)
ax.errorbar(csX, csCent[0], fmt='ro', markersize=3, ecolor='black', capsize=2,)
ax.set_xlabel('Trial')
ax.set_ylabel('Bin Number')
ax.set_title('Stability Test with Cs-137')
ax.legend()
fig.set_dpi(300)
fig.tight_layout()
fig.savefig('stability.png')

mgLambda = []
mgLambdaUn = []
naLambda = []
naLambdaUn = []
alLambda = []
alLambdaUn = []


for i in range(2):
    mgPopt, mgPcov = curve_fit(halfLife, mgTime[i], unumpy.nominal_values(
        mgData[i]), mg[3][i], absolute_sigma=True, sigma=unumpy.std_devs(mgData[i]))
    naPopt, naPcov = curve_fit(
        halfLife, naTime[i], unumpy.nominal_values(naData[i]), na[3][i])
    alPopt, alPcov = curve_fit(halfLife, alTime[0], unumpy.nominal_values(
        alData[0]), al[3][0], absolute_sigma=True, sigma=unumpy.std_devs(alData[0]))
    #print(halfLife(mgTime[0], *mgPopt))
    option = [[mgData, mgTime, mgPopt, mgPcov, mg], [naData, naTime,
                                                     naPopt, naPcov, na], [alData, alTime, alPopt, alPcov, al]]
    for j in range(3):
        if j == 2:
            if i == 1:
                continue
        plotX = np.array(option[j][1][i])
        lineX = np.linspace(0, np.max(plotX), num=1000)
        plotY = np.array(unumpy.nominal_values(option[j][0][i]))
        yUn = unumpy.std_devs(option[j][0][i])
        popt = option[j][2]
        pcov = option[j][3]
        func = halfLife(np.array(plotX), *popt)
        poptUp = np.array(popt) + np.sqrt(np.diag(pcov))
        poptDown = np.array(popt) - np.sqrt(np.diag(pcov))
        lab = 'I = '+str("%.3f" % popt[0])+'*e^(-'+str("%.3f" %
                                                       popt[1])+'*x)+'+str("%.3f" % popt[2])
        fileName = option[j][4][4][i]+'.png'
        title = option[j][4][4][i]
        if j == 0:
            mgLambda.append(popt[1])
            mgLambdaUn.append(np.sqrt(np.diag(pcov))[1])
        elif j == 1:
            naLambda.append(popt[1])
            naLambdaUn.append(np.sqrt(np.diag(pcov))[1])
        elif j == 2:
            alLambda.append(popt[1])
            alLambdaUn.append(np.sqrt(np.diag(pcov))[1])
        #print(title)
        #print(popt)
        #print(np.sqrt(np.diag(pcov)))
        '''
        halflife = np.log(2)/popt[1]
        print(halflife, np.log(2)/popt[1])
        print('Seconds:', halflife)
        print('Minutes:', halflife/60)
        print('Hours:', halflife/3600)
        '''
        fig = plt.figure()
        ax = fig.subplots()
        ax.errorbar(lineX, halfLife(np.array(lineX), *poptUp), fmt='k-',
                    label='Uncertainty due to the standard deviation of the parameters')
        ax.errorbar(lineX, halfLife(np.array(lineX), *poptDown), fmt='k-')
        ax.errorbar(lineX, halfLife(np.array(lineX), *popt),
                    fmt='g--', label=lab)
        ax.errorbar(plotX, plotY, yerr=yUn,
                    fmt='ro', markersize=3, ecolor='black', capsize=2,)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Intensity (counts per second)')
        ax.set_title(title)
        ax.legend()

        fig.set_dpi(300)
        fig.tight_layout()
        fig.savefig(fileName)

mgLamAvg = np.average(mgLambda, weights=mgLambdaUn)
naLamAvg = np.average(naLambda, weights=naLambdaUn)
alLamAvg = np.average(alLambda, weights=alLambdaUn)
'''
print(mgLambda, mgLambdaUn)
print(mgLamAvg, np.average(mgLambdaUn))
print(np.log(2)/mgLamAvg/60)
print(np.log(2)/uncertainties.ufloat(mgLamAvg, np.average(mgLambdaUn))/60)
print(naLambda, naLambdaUn)
print(naLamAvg, np.average(naLambdaUn))
print(np.log(2)/naLamAvg/3600)
print(np.log(2)/uncertainties.ufloat(naLamAvg, np.average(naLambdaUn))/3600)
print(alLambda, alLambdaUn)
print(alLamAvg, np.average(alLambdaUn))
print(np.log(2)/alLamAvg/60)
print(np.log(2)/uncertainties.ufloat(alLamAvg, np.average(alLambdaUn))/60)
'''

calibEn = np.array([661.7, 1173, 1274, 1332, 1460, 2614])
calibBin = np.array([398, 694, 753, 787, 861, 1530])
calibLine = np.linspace(0, 2048)
calibPopt, calibPcov = curve_fit(stability, calibBin, calibEn)
#print(np.sqrt(np.diag(calibPcov)))
fig = plt.figure()
ax = fig.subplots()
ax.errorbar(calibLine, stability(np.array(calibLine), *calibPopt),
            fmt='g--', label='Energy = '+str("%.3f" % calibPopt[0])+' * Bin + '+str("%.3f" % calibPopt[1]))
ax.errorbar(calibBin, calibEn,
            fmt='ro', markersize=3, ecolor='black', capsize=2,)
ax.set_xlabel('Bin Number')
ax.set_ylabel('Energy (keV)')
ax.set_title('Calibration Plot')
ax.legend()
fig.set_dpi(300)
fig.tight_layout()
fig.savefig('calibration.png')
chi2 = np.sum(np.power(calibEn - stability(calibBin, *calibPopt),
              2)/stability(calibBin, *calibPopt))
#print(chi2)
