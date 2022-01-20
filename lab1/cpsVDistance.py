import numpy as np
import matplotlib.pyplot as plt
import uncertainties
from uncertainties import unumpy

def CreateErrorBar(x, y, xerr=None, yerr=None, fmt='', ecolor=None, elinewidth=None, capsize=None, capthick=None, barsabove=False, label=None):
    return[x, y, xerr, yerr, fmt, ecolor, elinewidth, capsize, capthick, barsabove, label]

# Plot formatted data
def CreatePlot(dataNum, data, xLabel, yLabel, Title, fileName):
    fig = plt.figure()
    ax = fig.subplots(1, 1)
    legendBool = False
    for i in range(dataNum):
        ax.errorbar(data[i][0], data[i][1],
                    xerr=data[i][2],
                    yerr=data[i][3],
                    label=data[i][10],
                    fmt=data[i][4],
                    ecolor=data[i][5],
                    elinewidth=data[i][6],
                    capsize=data[i][7],
                    capthick=data[i][8],
                    barsabove=data[i][9]
                    )
        if data[i][10]:
            legendBool = True
    ax.set_title(Title)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    if legendBool:
        ax.legend()
    fig.set_dpi(300)
    fig.savefig(fileName)


cps = [405.09,306.04,261.72,225.91,189.93,152.59,120.96,94.86,80.28,65.85,52.24]
cpsError =[]
for i in cps:
    cpsError.append(i*0.02)
cpsErr = unumpy.uarray(cps,cpsError)
distance = [6.3,7.8,9.4,10.2,11.7,12.5,14.6,16.6,18.5,20.9,23.9]
distError = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
distanceErr = unumpy.uarray(distance,distError)

model = np.polyfit(unumpy.nominal_values(distanceErr),unumpy.nominal_values(cpsErr),2)
print(model)
#predict = np.polyid(model)

#data1 = CreateErrorBar(unumpy.nominal_values(distanceErr),cps,xerr=unumpy.std_devs(distanceErr),fmt='o')
#CreatePlot(1,data1,'Distance from Detector (cm)','Counts per Second (s^-1)','Test of R^-2','inverseRSquared.png')
fig = plt.figure()
ax = fig.subplots(1, 1)
ax.errorbar(unumpy.nominal_values(distanceErr),unumpy.nominal_values(cpsErr),xerr=unumpy.std_devs(distanceErr),yerr=unumpy.std_devs(cpsErr),fmt='o',ecolor='black')
fig.savefig('inverseRSquared.png')
print(unumpy.std_devs(distanceErr))
print(unumpy.std_devs(cpsErr))
