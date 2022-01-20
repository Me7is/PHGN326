# Plot spectrum from MCA  spe file
# For PHGN 326 - Advanced Lab II
# Colorado School of Mines
# Author: Dan Shields
#
# Modifications made by:
#
#    Date:

import matplotlib.pyplot as plt
import numpy as np

directory_in = './'
filename1 = 'Background Energy Spectra 20cm 10min'
filename2 = 'Co60 Energy Spectra 20cm 10min' # Specify the import file name of SPE file
extention_in = '.Spe'

directory_out = './'
extention_out = '.pdf'


plt.title('Cs-137pectrum')
plt.xlabel('Bin Number', fontsize = 14) # Labeling the x-axis
plt.ylabel('Counts', fontsize = 14) # Labeling the y-axis

plt.xlim(0,2047) # Specifying x-plot range

with open(filename1+'.Spe') as inspec:
    _hit1 = []
    for line in inspec:
        if not "0 2047\n" in line:
            continue
        for line in inspec:
            if "$ROI:\n" in line:
                break
            _hit1.append(np.int(line))
    _bin = list(range(0,len(_hit1)))

with open(filename2+'.Spe') as inspec:
    _hit2 = []
    for line in inspec:
        if not "0 2047\n" in line:
            continue
        for line in inspec:
            if "$ROI:\n" in line:
                break
            _hit2.append(np.int(line))
    _bin2 = list(range(0,len(_hit2)))
#data=zip(_bin,_hit)
#print(list(data))
_hit = []
for i in range(len(_hit1)):
    _hit.append(_hit2[i]-_hit1[i])

plt.fill(_bin,_hit, "o")


plt.savefig(directory_out + 'Co60 and Background Difference' + extention_out, bbox_inches=0, dpi=600)

plt.show() # Displays the current figure on the screen
