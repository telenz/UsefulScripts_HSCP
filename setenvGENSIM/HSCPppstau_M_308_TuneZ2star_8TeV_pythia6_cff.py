FLAVOR = 'stau'
COM_ENERGY = 8000. 
MASS_POINT = 308   # GeV
PROCESS_FILE = 'SimG4Core/CustomPhysics/data/RhadronProcessList.txt'
PARTICLE_FILE = 'test/HSCPprod/data/particles.txt' 
SLHA_FILE = 'test/HSCPprod/data/pMSSM12_MCMC1_45_795878.slha'
PDT_FILE = 'test/HSCPprod/data/hscppythiapdt.tbl'  

import FWCore.ParameterSet.Config as cms

source = cms.Source("EmptySource")

from Configuration.Generator.PythiaUEZ2starSettings_cfi import *

generator = cms.EDFilter("Pythia6GeneratorFilter",
	pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.),
    comEnergy = cms.double(COM_ENERGY),
    crossSection = cms.untracked.double(-1),
    maxEventsToPrint = cms.untracked.int32(0),
    stopHadrons = cms.bool(False),
    gluinoHadrons =  cms.bool(False),  
                         
	PythiaParameters = cms.PSet(
	    pythiaUESettingsBlock,
		processParameters = cms.vstring(
                  'MSEL=0                   ! full user control ',
                  'MSUB(226)=1              ! Chipm-Chipm', 
		  'IMSS(1) = 11             ! Spectrum from external SLHA file',
		  'IMSS(21) = 33            ! LUN number for SLHA File (must be 33)',
		  'IMSS(22) = 33            ! Read-in SLHA decay table ',
		  'MDCY(C1000024,1)=0       ! set the chargino stable.'
		  ),
    SLHAParameters = cms.vstring('SLHAFILE = %s' % SLHA_FILE),
    parameterSets = cms.vstring(
    'pythiaUESettings', 'processParameters','SLHAParameters'),
    
    )
 )
                         
generator.hscpFlavor = cms.untracked.string(FLAVOR)
generator.massPoint = cms.untracked.int32(MASS_POINT)
generator.slhaFile = cms.untracked.string(SLHA_FILE)
generator.processFile = cms.untracked.string(PROCESS_FILE)
generator.particleFile = cms.untracked.string(PARTICLE_FILE)
generator.pdtFile = cms.FileInPath(PDT_FILE)

ProductionFilterSequence = cms.Sequence(generator)
