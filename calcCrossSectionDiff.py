#!/usr/bin/env/python

import ROOT as rt

from ROOT import gStyle
from ROOT import gROOT
from ROOT import TMath
from ROOT import TGraphAsymmErrors

import glob,gzip
import numpy as n

import sys
##############################################################################################################
##############################################################################################################

### Read limit file ########################################################################################
openFile = "sourceFiles/Compare_CrossSections_with_diff_Mixing.txt"
# read in the file as a list of lines
FILE = open(openFile)
lines = FILE.read().split("\n")
FILE.close()
# your data
dataXsec = []

# read the header
columnnames = lines[0].split()
# loop over the lines
for l in range(1,len(lines)):
    line = lines[l]
    # split the line
    columns = line.split()
    # skip empty lines
    if len(columns) == 0:
        continue
    # check that you have as many columns as columnnames
    if not len(columns) == len(columnnames):
        print "ERROR: number of columns in line{0} != number of columns in header line"
        sys.exit()
 
    # fill a dictionary:
    _data = dict()
    for c in range(0,len(columns)):
        number = columns[c]
        if c == 0:
            shorten = columns[c].split("_width")[0]
            number  = shorten[(len(shorten)-3):]
                    
        _data[columnnames[c]] = float(number)
    
    # add it to the data array
    dataXsec.append(_data)

print dataXsec
f  = open('HiggsinoWinoCrossSection.txt', 'w')
f.write('MASS  HIGGSINOLIKE  WINOLIKE\n')
### Fill graphs ########################################################################################
for m in range(0,7):

    mass = m*100 +100
    higgsinoMean = 0
    winoMean     = 0
    i=0
    for _dataXsec in dataXsec:
        print _dataXsec
        if _dataXsec['SAMPLE'] == mass:
            print "in"
            higgsinoMean = higgsinoMean + _dataXsec["HIGGSINOLIKE"]
            winoMean = winoMean + _dataXsec["WINOLIKE"]
            i= i+1

    higgsinoMean = (higgsinoMean/i)*10**9
    winoMean     = (winoMean/i)*10**9

    f.write(str(mass) + '  ' + str(higgsinoMean) + '  ' + str(winoMean) + '\n')

