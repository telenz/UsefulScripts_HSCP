#!/usr/bin/env/python

# Script to rename TTree name
# author: Teresa Lenz

import glob,gzip
import os
from os import rename
import ROOT as rt

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
	return parts


workdir = "results/"
#workdir = ""

os.chdir(workdir)

# list all output dirs
outputdirs = sorted(glob.glob("pMSSM12_MCMC1_30_549144_m*"), key=numericalSort)
print "found",len(outputdirs),"jobs"
print outputdirs
print ""

# loop over output files
for outputdir in outputdirs[0:1000]:

	
	f = rt.TFile(outputdir,"update");
	T = rt.TTree = f.Get("Events");
	T.Write(outputdir.split(".root")[0]);
    
