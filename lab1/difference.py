# Plot spectrum from MCA  spe file
# For PHGN 326 - Advanced Lab II
# Colorado School of Mines
# Author: Dan Shields
#
# Modifications made by: Larence Wiencke
#    added command line parser with various options
#    Date: Jan 20 2019

import matplotlib.pyplot as plt
import numpy as np
import argparse
from operator import sub
import os, sys
import time
import datetime


parser = argparse.ArgumentParser(description="Plot Spectrum of 2 Spe files and difference")
parser.add_argument("-if1", "--infile1",
                    help="filename of spe file 1, for example ex4_file1.Spe",
                    required=True)
parser.add_argument("-if2", "--infile2",
                    help="filename of spe file 2, for example ex4_file2.Spe",
					  required=True)
parser.add_argument("-of", "--outfile",
                    help="filename for plot file ie figure1.pdf or figure2.png")
parser.add_argument("-x", "--xlabel",
                    default="Bin Number",
                    help="label for the x axis")
parser.add_argument("-y", "--ylabel",
                    default="Counts",
                    help="label for the y axis")
parser.add_argument("-xl", "--xbinlower", type=int,
                    default=0,
						help="lower bin number")
parser.add_argument("-xu", "--xbinupper", type=int,
                    default=2047,
						help="upper bin number")
parser.add_argument("-yl", "--ybinlower", type=float,
                    default=0.1,
						help="lower count number (must be >0.0 for -log option)")	#careful for semilog
parser.add_argument("-yu", "--ybinupper", type=float,
                    default=-1,
						help="upper count number")
parser.add_argument("-g", "--grid", action='store_true',
						help="to add gridlines")
parser.add_argument("-s", "--one", action='store_true',
						help="single plot (superimpose data)")
parser.add_argument("-log", "--ylog", action='store_true',
						help="to plot semilog (y axis log scale)")
parser.add_argument("-ms", "--markersize", type=int,
                    default=1,
					    help="Marker Size for points in plot")
parser.add_argument("-id", "--info", action='store_true',
					    help="Add date and other info to top of figure")

print("Starting...")

infile1 = parser.parse_args().infile1
infile2 = parser.parse_args().infile2
outfile = parser.parse_args().outfile
xlabel = parser.parse_args().xlabel
ylabel = parser.parse_args().ylabel
xbinlower = parser.parse_args().xbinlower
xbinupper = parser.parse_args().xbinupper
ybinlower = parser.parse_args().ybinlower
ybinupper = parser.parse_args().ybinupper
grid=parser.parse_args().grid
one=parser.parse_args().one
ylog=parser.parse_args().ylog
mrksz=parser.parse_args().markersize
info=parser.parse_args().info

print( "input file 1 is:", infile1)
print( "input file 2 is:", infile2)
print(" output plot is:", outfile)
print(parser.parse_args())  #prints out all the commandline parameters

#put date and other info on the top of plot if -id selected
now = datetime.datetime.now()
if info: plt.suptitle(str(now.strftime("%Y-%m-%d %H:%M:%S")+"  "
+os.path.basename(sys.argv[0])+" "+infile1+" "+infile2+"  "+outfile),
ha='center',size=9)

#set number of plots on figure
three = True  #default is 3 separate plots
fz = np.int(12) #font size of axis labels
lz = np.int(8)  #font size of numbers along the axis

if(one):
	three = False  #if -s selected turn off three
	fz = np.int(14)  #and use a larger fontsize
	lz = np.int(10)

ylin = True
if ylog: ylin = False #turn off linear plot if log selected

#default value of ybinupper is negative
#if it is not negative, it means the user set it through the command line
#in this case use plt.ylim to set it, if not dont call plt.ylim and ylim is set by the data
if ybinupper>0:plt.ylim(ybinlower,ybinupper) # Specifying y-plot range (counts)

#open file 1 and read in data
with open(infile1) as inspec:
    _hit1 = []
    for line in inspec:
        if not "0 2047\n" in line:
            continue
        for line in inspec:
            if "$ROI:\n" in line:
                break
            _hit1.append(np.int(line))
    _bin1 = list(range(0,len(_hit1)))

#open file 2 and read in data
with open(infile2) as inspec:
    _hit2 = []
    for line in inspec:
        if not "0 2047\n" in line:
            continue
        for line in inspec:
            if "$ROI:\n" in line:
                break
            _hit2.append(np.int(line))
    _bin2 = list(range(0,len(_hit2)))

#Subtract the histograms (file1-file2)
#"... the determined Real Programmer can write FORTRAN programs in any language."
#Post, Ed (July 1983). "Real Programmers Don't Use Pascal". Datamation.
#
_hit3 = [] #declare an array to hold the counts
_bin3 = [] #declare an array to hold the bin number
for x in range(0,min(len(_hit1),len(_hit2))):
	#print(x,_hit1[x],_hit2[x],_hit1[x]-_hit2[x])
	_bin3.append(np.int(x))
	_hit3.append(np.int(x))
	_bin3[x]=x #the bin number
	_hit3[x]=_hit1[x]-_hit2[x]  #subtract the contents of the histograms
	#print("bin3 and hit3:", _bin3[x], _hit3[x])

#make the plots

if three: plt.subplot(3, 1, 1)  #top plot of the three
plt.xlim(xbinlower,xbinupper) # Specifying x-plot range (2047 is max for MCA)
if ybinupper>0:plt.ylim(ybinlower,ybinupper) # Specifying y-plot range (counts)
plt.ylabel(ylabel, fontsize = fz) # Labeling the y-axis
plt.tick_params(axis='both', labelsize = lz)
plt.grid(grid) #note grid option is set to True by -g in commandline parsing
if one:
	plt.xlabel(xlabel, fontsize = fz) # Labeling the x-axis if one plot (skip for top two of three plots option)
	plt.tick_params(axis='both', labelsize = lz)
if 	ylog: plt.semilogy(_bin1,_hit1, 'b', label='file1',linestyle='none',marker='.',markersize=mrksz)
if 	ylin: plt.plot(_bin1,_hit1, 'b', label='file1',linestyle='none',marker='.',markersize=mrksz)
if three: legend = plt.legend(loc='upper right', shadow=True, fontsize='medium', markerscale=5)
if three:
	plt.subplot(3,1,2)
	plt.grid(grid)
	plt.ylabel(ylabel, fontsize = fz)
	plt.tick_params(axis='both', labelsize = lz)
	plt.xlim(xbinlower,xbinupper)
	if ybinupper>0:plt.ylim(ybinlower,ybinupper) # Specifying y-plot range (counts)
if ylog: plt.semilogy(_bin2,_hit2, 'g',label='file2', linestyle='none',marker='.',markersize=mrksz)
if ylin: plt.plot(_bin2,_hit2, 'g',label='file2', linestyle='none',marker='.',markersize=mrksz)
if three: legend = plt.legend(loc='upper right', shadow=True, fontsize='medium', markerscale=5)

if three:
	plt.subplot(3,1,3)
	plt.grid(grid)
	plt.ylabel(ylabel, fontsize = fz)
	plt.xlabel(xlabel, fontsize = fz) # Labeling the x-axis
	plt.tick_params(axis='both', labelsize = lz)
	plt.xlim(xbinlower,xbinupper)
	if ybinupper>0:plt.ylim(ybinlower,ybinupper) # Specifying y-plot range (counts)
if ylog: plt.semilogy(_bin3,_hit3, 'r', label='difference',linestyle='none',marker='.',markersize=mrksz)
if ylin: plt.plot(_bin3,_hit3, 'r', label='difference',linestyle='none',marker='.',markersize=mrksz)
if three: legend = plt.legend(loc='upper right', shadow=True, fontsize='medium', markerscale=5)
if one: legend = plt.legend(loc='upper right', shadow=True, fontsize='large', markerscale=5)



#os.path.basename(sys.argv[0])
#save the plot to a file recommend: .pdf or .png format
#the file has vector graphics (doen't get blury when you blow it up)
#much better to use this file rather than a screen shot in a report
if outfile:
	plt.savefig(outfile, bbox_inches=0, dpi=600)

plt.show() # Displays the current figure on the screen
