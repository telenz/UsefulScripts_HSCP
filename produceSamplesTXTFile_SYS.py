#!/usr/bin/env/python

import glob,gzip
import os

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
	return parts


workdir = "/scratch/hh/dust/naf/cms/user/telenz/grid-control-For-HSCP/parameter_scan/grid-control/work.job_9"
slhapattern = "export SLHANAME="
xsectionpattern = "All included subprocesses"
decaywidthpattern = "pdgID, width 1000024,  "
rootfilenamepattern = 'export SE_OUTPUT_PATTERN="'
print decaywidthpattern
#decaywidthpattern = "DecayTable"

# list all output dirs
outputdirs = sorted(glob.glob(workdir + "/output/job_*"), key=numericalSort)
print "found",len(outputdirs),"jobs"

# dictionary with cross sections
xsect = dict()

f     = open('Analysis_Samples_SYS.txt', 'w')
f2    = open('Analysis_Samples_withWidth_SYS.txt', 'w')
fCuts = open('Analysis_Cuts_SYS.txt', 'w')

# loop over output files
for outputdir in outputdirs[0:1000]:   
    
    # which is the slha file used?
    FILE = open(outputdir + "/gc.stdout")
    lines = FILE.read().split("\n")
    FILE.close()
    slhaname = ""
    for line in lines:
        if line.find(slhapattern) == 0:
            slhaname = line[len(slhapattern):-1].strip("\"")
            print slhaname
            break
    break
   

for outputdir in outputdirs[0:1000]:

    jobNr = outputdir.split('output/job_')[1]
    rootfileName = ""
    f.write('"CMSSW_5_3",  2, ')

    FILE = open(outputdir + "/gc.stdout")
    lines = FILE.read().split("\n")
    FILE.close()
    for line in lines:
        if line.find(rootfilenamepattern) == 0:
	    print line[len(rootfilenamepattern):-1]
	    rootfileName = line[len(rootfilenamepattern):-1].split(".root")[0]
            print rootfileName
	    
	    part2 = rootfileName.split("_")[6]
	    nameFinal = rootfileName[:(len(rootfileName)-len(part2)-1)]
	    print nameFinal
	    print ""
            break


    f.write('"' + str(nameFinal) + '"')
    f2.write('"' + str(nameFinal) + '"')
    fCuts.write('"' + str(nameFinal) + '"')
    fCuts.write(", 0,  70.0, 0.400, 0.000, 1 \n")
    fCuts.write('"' + str(nameFinal) + '"')
    fCuts.write(", 2,  70.0, 0.125, 1.225, 1 \n")
    
         
    f.write(' ,"' + str(nameFinal) + '"  ')
            
    f.write(' , "MC: Chipm Width ')
    #f.write(str(int(jobNr)%5) + ' ' + str(int(jobNr)/5*100+100))
    f.write(nameFinal.split("width")[1])
    massAux = nameFinal.split("_width")[0]
    mass    = massAux.split("_m")[1]    
    f.write(' GeV/#font[12]{c}^{2}"   , "S10"  , ')
    f.write(str(mass))
    #f.write(str(int(jobNr)/5*100+100))
    f.write(',   ')
    
    # which is the slha file used?
    FILE = open(outputdir + "/gc.stdout")
    lines = FILE.read().split("\n")
    FILE.close()
    for line in lines:
        if line.find(slhapattern) == 0:
            slhaname2 = line[len(slhapattern):-1].strip("\"")
            #print slhaname2
            break
    if slhaname2 != slhaname:     
        continue

    # find cross section
    FILE = gzip.open(outputdir + "/cmssw.log.gz", 'rb')
    lines = FILE.read().split("\n")
    FILE.close()

    for l in range(len(lines)):
        l += 1
        line = lines[l]
        if line.find(xsectionpattern) > 0:
            elements = line.split("I")
            _xsect = float(elements[-2].replace("D","e"))
            print "Cross-section  = " + str(_xsect)
            f.write("+"+str('%0.7E' %(_xsect/10**-9)))
            #xsect[slhaname].append(_xsect)
            break

    for l in range(len(lines)-1):
        l += 1
        #print l
        line = lines[l]
        #print line
        if line.find(decaywidthpattern) > 0:
            elements = line.split("width 1000024,  ")
            print elements[1]
            _Tau = float(elements[1].replace("E","e"))
            print "Decay Width = " + str(_Tau)
            break


    f.write(' , 1, 1.000, 1.000, 1.000  ')
    f.write("\n")

    f2.write('  ,' + str('%0.7E' %(_Tau)))
    f2.write("\n")
    
