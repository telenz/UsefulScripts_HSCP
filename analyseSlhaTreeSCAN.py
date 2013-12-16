#!/usr/bin/env python

import math

import ROOT as rt
import os

filename = "sourceFiles/pMSSM12_MCMC1_120mh130_56p2K_humanReadable.root"
print "opening file '" + filename + "'..."
file = rt.TFile.Open(filename)

treename = "slha"
print "reading tree '" + treename + "'..." 
tree = file.Get(treename)

print "looping over tree..."

# speed of light [m/s]
c0 = 2.9979*10**(8)
# hbar [eV/s]
hbar = 6.5821*10**(-24)
# Energy [eV]
E = 1.333333*10**12
# different length [m]

sBeamPipe              = 0.04
sMiddTracker           = 0.6
sAfterTracker          = 1.1
sFirstLayerMuonChamber = 4
sFullDetector          = 10

sListLowerBounds = [0.01,0.1,1.1,3.5,10]
sListUpperBounds = [0.04,1.1,3.0,4.8,30000]

sListDecayWidth  = [0.0,0.0,0.0,0.0,0.0]

for s in range(0,len(sListLowerBounds)):
    print sListLowerBounds[s]
    print sListUpperBounds[s]

printCommand = 0
nEvents = 10000
split =  10

nMassPoints = 7

minMass = 100
maxMass = 700

counts = 0
minWidth = 100000
maxWidth = 0
saveSLHAName = 'test'

slhaFilesDir = '/scratch/hh/dust/naf/cms/user/lveldere/pMSSM13/data/slha/pMSSM12_MCMC1_120mh130_56p2K'

f = open('parametersSCAN.txt', 'w')

f.write("RUNNUMBER,LUMINUMBER,NEVENTS,SLHANAME,SAVEFILENAME,CHARGINOMASS,DECAYWIDTH,NEUTRALINOMASS\n")

for i in range(1,2):
    Width = 100
    
    lowMass  = 100 + i*100
    lowMass  = lowMass  - 10#0.05*lowMass 
    highMass = 100 + i*100
    highMass = highMass + 10#0.05*highMass

    print "i=0 ",i,":  lowMass = ",lowMass,":   highMass = ",highMass,"\n"
    
    for e in range(0,tree.GetEntries()):
        
        tree.GetEntry(e)
        
        
        if (tree.mass_h < 124.0) | (tree.mass_h > 126.0):
            continue

        if (tree.mass_sW1 < lowMass) | (tree.mass_sW1 > highMass):
            continue

        if (abs(tree.decay_sW1_tw/(10**(-16))-1) < Width):
            saveSLHAfilename  = tree.slhapath
            saveSLHAName      = os.path.split(tree.slhapath)[1]
            saveCharginoMass   = tree.mass_sW1
            saveNeutralinoMass = tree.mass_sZ1
            saveDecayWidth   = tree.decay_sW1_tw
            Width    = abs(tree.decay_sW1_tw/(10**-16)-1)
            
            continue
        else:
            continue

print "Slha name = '" + saveSLHAName + "' "
print "Chargino decay width = " + str(saveDecayWidth)
print "Chargino mass = " + str(saveCharginoMass)
print "Neutralino mass = " + str(saveNeutralinoMass)
print "stau mass = " + str(tree.mass_stau_1)
print "stau mass = " + str(tree.mass_stau_2)
print "stop mass = " + str(tree.mass_st_1)
print "stop mass = " + str(tree.mass_st_2)
Chi0ChipmMassDiff = saveCharginoMass-saveNeutralinoMass
if (Chi0ChipmMassDiff < 0.1400000):
    Chi0ChipmMassDiff = 0.1400000
print "Chargino - Neutralino mass difference = " + str(Chi0ChipmMassDiff)
print ""
for i in range(0,nMassPoints):   
    for s in range(0,len(sListLowerBounds)):
        for c in range(0,split):
            charginomass = minMass+i*100
            decayWidth = hbar * c0 /(sListUpperBounds[s]-sListLowerBounds[s])*math.sqrt(1-(300*10**(9)/E)**2)*math.log(sListUpperBounds[s]/sListLowerBounds[s])
            sListDecayWidth[s] = decayWidth
            lifetime = hbar/decayWidth
                    
    counts = counts + 1


print sListDecayWidth

distance = (sListDecayWidth[4]-sListDecayWidth[3])/6
sListDecayWidthNew = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]

for s in range(0,len(sListDecayWidthNew)):
    sListDecayWidthNew[s] = sListDecayWidth[3] + (s)*distance

print sListDecayWidthNew


for i in range(0,nMassPoints):   
    for s in range(0,len(sListDecayWidthNew)):
        for c in range(0,split):
            f.write(str((i*len(sListDecayWidthNew)+1)+s))
            f.write(",")
            f.write(str(c*nEvents/split+1))
            f.write(",")
            f.write(str(nEvents/split))
            f.write(",")
            f.write(saveSLHAName.replace(".slha",""))
            f.write(",")
            f.write("m")
            charginomass = minMass+i*100
            f.write(str(charginomass))
            f.write("_width")
            f.write(str(s))
            f.write(",")
            f.write(str(charginomass))
            f.write(",")            
            f.write(str('%0.7E' %sListDecayWidthNew[s]))
            f.write(",")
            f.write(str(charginomass-Chi0ChipmMassDiff))
            f.write("\n")
