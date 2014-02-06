import FWCore.ParameterSet.Config as cms

def customise(process):
    
	FLAVOR = process.generator.hscpFlavor.value()
	MASS_POINT = process.generator.massPoint.value()
	SLHA_FILE = process.generator.slhaFile.value()
	PROCESS_FILE = process.generator.processFile.value()
	PARTICLE_FILE = process.generator.particleFile.value()
	PDT_FILE = process.generator.pdtFile.value()
#	USE_REGGE = process.generator.useregge.value()

	process.HepPDTESSource.pdtFileName= PDT_FILE
	

	return process
	
