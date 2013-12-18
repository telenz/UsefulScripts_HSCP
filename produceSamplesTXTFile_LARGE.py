#!/usr/bin/env/python

import glob,gzip
import os

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
	return parts


workdir = "/scratch/hh/dust/naf/cms/user/telenz/grid-control-For-HSCP/parameter_scan/grid-control/work.job_8"
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
samples = list()

f     = open('Analysis_Samples_LARGE.txt', 'w')
f2    = open('Analysis_Samples_withWidth_LARGE.txt', 'w')
fCuts = open('Analysis_Cuts_LARGE.txt', 'w')

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

i = 0
firstTime = 1
for outputdir in outputdirs[0:1000]:

    FILE = open(outputdir + "/gc.stdout")
    lines = FILE.read().split("\n")
    FILE.close()
    for line in lines:
        if line.find(rootfilenamepattern) == 0:
	    #print line[len(rootfilenamepattern):-1]
	    rootfileName = line[len(rootfilenamepattern):-1].split(".root")[0]
            #print rootfileName
	    
	    part2 = rootfileName.split("_")[6]
	    nameFinal = rootfileName[:(len(rootfileName)-len(part2)-1)]
	    #print nameFinal
	    #print ""
	    if firstTime==1:
		    samples.append(nameFinal)
		    firstTime = 0
	    elif nameFinal != samples[i]:
		    samples.append(nameFinal)
		    i = i+1
            break



for _samples in samples[0:1000]:

	print _samples
	xsect = 0;
	numberOfJobs = 0.0
	_xsect = 0.0
	_Tau   = 0.0
	for outputdir in outputdirs[0:1000]:

		# Read File:
		FILE = open(outputdir + "/gc.stdout")
		lines = FILE.read().split("\n")
		FILE.close()

		# Check which sample it is:
		for line in lines:
			if line.find(rootfilenamepattern) == 0:
				rootfileName = line[len(rootfilenamepattern):-1].split(".root")[0]
				#print rootfileName
	                        break 

		if not _samples in rootfileName: continue

		numberOfJobs = numberOfJobs + 1.0

		# Read other file:
		FILE = gzip.open(outputdir + "/cmssw.log.gz", 'rb')
		lines = FILE.read().split("\n")
		FILE.close()

		for line in lines:
			if line.find(xsectionpattern) > 0:
				elements = line.split("I")
				_xsect = float(elements[-2].replace("D","e"))
				print "Cross-section  = " + str(_xsect)
				break

		for line in lines:

			if line.find(decaywidthpattern) > 0:
				elements = line.split("width 1000024,  ")
				_Tau = float(elements[1].replace("E","e"))
				print "Decay Width = " + str(_Tau)
				break
            
		xsect = xsect+_xsect
		print _xsect
		print xsect
	xsect = xsect/numberOfJobs
	
	# Start writing the files
	
	f.write('"CMSSW_5_3",  2, ')
	f.write('"' + str(_samples) + '"')
	f2.write('"' + str(_samples) + '"')
	fCuts.write('"' + str(_samples) + '"')
	fCuts.write(", 0,  70.0, 0.400, 0.000, 1 \n")
	fCuts.write('"' + str(_samples) + '"')
	fCuts.write(", 2,  70.0, 0.125, 1.225, 1 \n")
	f.write(' ,"' + str(_samples) + '"  ')
	f.write(' , "MC: Chipm Width ')
	f.write(_samples.split("width")[1])
	f.write(' GeV/#font[12]{c}^{2}"   , "S10"  , ')
	massAux = _samples.split("_width")[0]
	mass    = massAux.split("_m")[1]    
	f.write(str(mass))
	f.write(',   ')
	f.write("+"+str('%0.7E' %(xsect/10**-9)))
	f.write(' , 1, 1.000, 1.000, 1.000  ')
	f.write("\n")
	f2.write('  ,' + str('%0.7E' %(_Tau)))
	f2.write("\n")


#print samples
