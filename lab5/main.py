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


createFig("Trial_1.spe", "Trial 1", "trial1.png")
createFig("Trial_2.spe", "Trial 2", "trial2.png")
createFig("Trial_3.spe", "Trial 3", "trial3.png")
createFig("Adlab Complex Sean and Kevin Data.spe",
          "Overnight", "overnight.png")
createFig("2022_03_31_alpha_gamma_1800s.spe", "30 Minutes", "short.png")
createFig("2022_03_31_alph_gam_cal_40ns_2p56us.Spe", 'Broken', "broken.png")
