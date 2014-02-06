#!/bin/bash
################################################################################################################
# Script to set up the CMSSW python config to create GEN_SIM samples with particles decayed via geant (T. Lenz)
#################################################################################################################

DIRECTORY="CMSSW_5_3_2_patch4"
if [ -d "$DIRECTORY" ]; then
echo "The CMSSW directory already exists."
return
fi
echo "------------------------------------"
echo "--- setting up CMSSW environment ---"
echo "------------------------------------"
cmsrel $DIRECTORY
cd $DIRECTORY/src
cmsenv

echo "------------------------------------"
echo "----------- Add packages -----------"
echo "------------------------------------"
git-cms-addpkg AnalysisDataFormats/SUSYBSMObjects
echo "------------------------------------"
git-cms-addpkg RecoMuon/MuonIdentification
echo "--------------------------------------------------------------------------------------"
git-cms-addpkg SUSYBSMAnalysis/HSCP
echo "--------------------------------------------------------------------------------------"
git fetch official-cmssw imported-CVS-HEAD:imported-CVS-HEAD
echo "--------------------------------------------------------------------------------------"
git checkout imported-CVS-HEAD -- SUSYBSMAnalysis/HSCP
echo "--------------------------------------------------------------------------------------"
git checkout imported-CVS-HEAD -- AnalysisDataFormats/SUSYBSMObjects
echo "--------------------------------------------------------------------------------------"
git cms-cvs-history import V02-02-34 Configuration/Skimming
echo "--------------------------------------------------------------------------------------"
git cms-cvs-history import V02-05-02 RecoLocalMuon/DTSegment
echo "--------------------------------------------------------------------------------------"
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvREDIGIRECO/HSCPDeDxInfoProducer.cc SUSYBSMAnalysis/HSCP/src/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvREDIGIRECO/CSCTimingExtractor.cc RecoMuon/MuonIdentification/src/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvREDIGIRECO/classes_def.xml AnalysisDataFormats/SUSYBSMObjects/src/.

#git cms-cvs-history import V02-02-03 HiggsAnalysis/CombinedLimit #not needed for Ntuples
#git-cms-addpkg HiggsAnalysis/CombinedLimit #-r V02-02-03
echo "------------------------------------"
echo "-------------- Compile -------------"
echo "------------------------------------"
scram b -j8
echo "------------------------------------"
echo "-- Run cmsDriver Command (REDIGI) --"
echo "------------------------------------"
cmsDriver.py REDIGI --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --conditions START53_V7A::All --pileup 2012_Summer_50ns_PoissonOOTPU  --datamix NODATAMIXER --filein=file:../../CMSSW_5_2_6_patch1/src/HSCPppstau_M_308_TuneZ2star_8TeV_pythia6_cff_py_GEN_SIM.root  --eventcontent RAWSIM --datatier GEN-SIM-RAW --no_exec -n  1

echo "# Needed for PU
process.mix.input.fileNames = fileNames = cms.untracked.vstring('file:/nfs/dust/cms/user/tlenz/PUrootFiles/1AD9E627-7316-E111-B3A5-001A9281173C.root',
                                                                'file:/nfs/dust/cms/user/tlenz/PUrootFiles/0477EED1-7516-E111-B834-0018F3D0962E.root',
                                                                'file:/nfs/dust/cms/user/tlenz/PUrootFiles/3E1F5CF3-DB16-E111-A7C7-001A928116CE.root')" >> REDIGI_DIGI_L1_DIGI2RAW_HLT_PU.py

echo "------------------------------------"
echo "--- Run cmsDriver Command (RECO) ---"
echo "------------------------------------"
cmsDriver.py RECO --step RAW2DIGI,L1Reco,RECO --conditions START53_V7A::All --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER  --filein=file:REDIGI_DIGI_L1_DIGI2RAW_HLT_PU.root --eventcontent RECOSIM --datatier GEN-SIM-RECO --no_exec -n  1
echo "------------------------------------"
echo "--------------- Finished -----------"
echo "------------------------------------"


# Please add also the following, if you want to keep the cross-sections in the sample 
# process.RAWSIMoutput.outputCommands.extend(["keep GenRunInfoProduct_*_*_*", "keep *_genParticles_*_*", "keep GenEventInfoProduct_generator_*_*"])