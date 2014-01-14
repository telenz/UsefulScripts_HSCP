#!/usr/bin/env/python

import glob,gzip
import os
import time
import re
import sys
numbers = re.compile(r'(\d+)')
def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
	return parts

now = time.time()

workdir             = "/nfs/dust/cms/user/tlenz/grid-control-For-HSCP/parameter_scan/grid-control/work.job_10"
slhapattern         = "export SLHANAME="
xsectionpattern     = "All included subprocesses"
decaywidthpattern   = "pdgID, width 1000024,  "
rootfilenamepattern = 'export SE_OUTPUT_PATTERN="'
print decaywidthpattern

# list all output dirs
outputdirs = sorted(glob.glob(workdir + "/output/job_*"), key=numericalSort)
print "found",len(outputdirs),"jobs"

# Create the three needed files
f     = open('Analysis_Samples_FULL.txt', 'w')
f2    = open('Analysis_Samples_withWidth_FULL.txt', 'w')
fCuts = open('Analysis_Cuts_FULL.txt', 'w')

# dict of different samples
samples = dict()

# Create dictionary with all samples and the corresponding paths to it
for outputdir in outputdirs[0:10000]:

    FILE = open(outputdir + "/gc.stdout")
    lines = FILE.read().split("\n")
    FILE.close()
    for line in lines:
        if line.find(rootfilenamepattern) == 0:
	    rootfileName = line[len(rootfilenamepattern):-1].split(".root")[0]
            
	    part2 = rootfileName.split("_")[6]
	    nameFinal = rootfileName[:(len(rootfileName)-len(part2)-1)]

	    if not nameFinal in samples:
		    samples.update([[nameFinal,[]]])
		    #print nameFinal


	    samples[nameFinal].append(outputdir)
	    break


# Sort again the samples and write them to a list (samples_sorted)
samples_sorted = sorted(samples, key=numericalSort)

# Loop over all samples and calculate the mean out of the various subsamples of the cross-section 
for _sample in samples_sorted:

	xsect        = 0;
	numberOfJobs = 0.0
	_xsect       = 0.0
	_Tau         = 0.0

	for _path in samples[_sample]:

		numberOfJobs = numberOfJobs + 1.0

		# Read cmssw log file for cross-section information
		FILE = gzip.open(_path + "/cmssw.log.gz", 'rb')
		lines = FILE.read().split("\n")
		FILE.close()

		for line in lines:
			if line.find(xsectionpattern) > 0:
				elements = line.split("I")
				_xsect = float(elements[-2].replace("D","e"))
				break

		for line in lines:
			if line.find(decaywidthpattern) > 0:
				elements = line.split("width 1000024,  ")
				_Tau = float(elements[1].replace("E","e"))
				break
            
		xsect = xsect+_xsect


	xsect = xsect/numberOfJobs
	
	# Write relevant information into the files
	f.write('"CMSSW_5_3",  2, ')
	f.write('"' + str(_sample) + '"')
	f2.write('"' + str(_sample) + '"')
	fCuts.write('"' + str(_sample) + '"')
	fCuts.write(", 0,  70.0, 0.400, 0.000, 1 \n")
	fCuts.write('"' + str(_sample) + '"')
	fCuts.write(", 2,  70.0, 0.125, 1.225, 1 \n")
	f.write(' ,"' + str(_sample) + '"  ')
	f.write(' , "MC: Chipm Width ')
	f.write(_sample.split("width")[1])
	f.write(' GeV/#font[12]{c}^{2}"   , "S10"  , ')
	massAux = _sample.split("_width")[0]
	mass    = massAux.split("_m")[1]    
	f.write(str(mass))
	f.write(',   ')
	f.write("+"+str('%0.7E' %(xsect/10**-9)))
	f.write(' , 1, 1.000, 1.000, 1.000  ')
	f.write("\n")
	f2.write('  ,' + str('%0.7E' %(_Tau)))
	f2.write("\n")

future = time.time()

print str('%.2f' %((future-now)/60.)) + " min have passed."
