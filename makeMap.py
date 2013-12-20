#!/usr/bin/env/python

import glob,gzip
import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts

#############################################################
AnalysisType = "Type2"
##############################################################

MassPattern         = "Mass         : "
LimitPatternObs     = "XSec_Obs     : "
LimitPatternExp     = "XSec_Exp     : "
LimitPatternExpUp   = "XSec_ExpUp   : "
LimitPatternExpDown = "XSec_ExpDown : "
XSectionPattern     = "XSec_Th      : "

f = open(str('MapTable_' + AnalysisType + '_LARGE.txt'), 'w')
f.write('INDEX  MASS  WIDTH  XSECTION  OBSLIMIT EXPLIMIT EXPLIMITUP EXPLIMITDOWN\n')
outputdir = str("Results/" + AnalysisType + "/EXCLUSION8TeV/")
analysisfile = "Analysis_Samples_withWidth.txt"

# list all output dirs
outputdirs = glob.glob(outputdir + "pMSSM*_m*_width*.txt")
outputdirs = sorted(glob.glob(outputdir + "pMSSM*_m*_width*.txt"), key=numericalSort)
print "found:",len(outputdirs),"output files"


for outputfile in outputdirs[0:1000]:

    # which is the slha file used?
    FILE = open(outputfile)
    scenarioFile = outputfile.split("EXCLUSION8TeV/")
    scenarioName = scenarioFile[1][0:-4]
    print scenarioName
    index = scenarioName[-3:]
    print "last chars :" + index
    print index.find("h")
    if index.find("_") >= 0:
        index2 = index.split("_")
    elif index.find("h") >= 0:
        index2 = index.split("h")
    print index2[1]
    lines = FILE.read().split("\n")
    FILE.close()
    mass = ""
    for line in lines:
        if line.find(MassPattern) == 0:
            mass = line[len(MassPattern):-1]
        elif line.find(LimitPatternObs) == 0:
            limitobs = line[len(MassPattern):-1]
            if(float(limitobs)>10**9):
                limitobs = -1
                #print "Limit too large"
        elif line.find(LimitPatternExp) == 0:
            limitexp = line[len(MassPattern):-1]
            if(float(limitexp)>10**9):
                limitexp = -1
                #print "Limit too large"
        elif line.find(LimitPatternExpUp) == 0:
            limitexpUp = line[len(MassPattern):-1]
            if(float(limitexpUp)>10**9):
                limitexpUp = -1
        elif line.find(LimitPatternExpDown) == 0:
            limitexpDown = line[len(MassPattern):-1]
            if(float(limitexpDown)>10**9):
                limitexpDown = -1
        elif line.find(XSectionPattern) == 0:
            xsec = line[len(XSectionPattern):-1]


    FILE = open(analysisfile)
    lines = FILE.read().split("\n")
    FILE.close()
    for line in lines:
        print line
        if line.find('"' + scenarioName + '"') == 0:
            width = float(line.split(",")[1])
            print width
        
    #print mass
    #print xsec
    #print limit
    #print ""
    f.write(str(index2[1]) + "  " + str(mass) + "  " + str('%0.7E' %(width)) + "  " + xsec + "  " + str(limitobs) +"  " + str(limitexp) +"  " + str(limitexpUp) +"  " + str(limitexpDown) + "\n")
    
