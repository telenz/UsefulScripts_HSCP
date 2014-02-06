#!/bin/bash
################################################################################################################
# Script to set up the CMSSW python config to create GEN_SIM samples with particles decayed via geant (T. Lenz)
#################################################################################################################

DIRECTORY="CMSSW_5_2_6_patch1"
if [ -d "$DIRECTORY" ]; then
echo "The CMSSW directory already exists."
return
fi
echo "------------------------------------"
echo "--- setting up CMSSW environment ---"
echo "------------------------------------"
cmsrel $DIRECTORY
cd CMSSW_5_2_6_patch1/src
cmsenv
git-cms-addpkg SimG4Core/CustomPhysics
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/CustomPDGParser.h SimG4Core/CustomPhysics/interface/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/CustomPDGParser.cc SimG4Core/CustomPhysics/src/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/CustomParticleFactory.cc SimG4Core/CustomPhysics/src/.

mkdir test
cd test
echo "------------------------------------"
echo "---------- Make new package --------"
echo "------------------------------------"
mkedanlzr HSCPprod
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/Exotica_HSCP_SIM_cfi.py HSCPprod/python/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/Exotica_HSCP_SIM_cfi_GEN.py HSCPprod/python/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/HSCPppstau_M_308_TuneZ2star_8TeV_pythia6_cff.py HSCPprod/python/.
cd ..
echo "------------------------------------"
echo "-------------- Compile -------------"
echo "------------------------------------"
scram b -j8
echo "------------------------------------"
echo "------ Run cmsDriver Command -------"
echo "------------------------------------"
cmsDriver.py test/HSCPprod/python/HSCPppstau_M_308_TuneZ2star_8TeV_pythia6_cff.py --step GEN,SIM --customise test/HSCPprod/Exotica_HSCP_SIM_cfi.customise --conditions START52_V9::All --pileup NoPileUp --datamix NODATAMIXER --beamspot Realistic8TeVCollision --datatier GEN-SIM --eventcontent RAWSIM -n 1 --no_exec

mkdir test/HSCPprod/data/
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/particles.txt test/HSCPprod/data/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/pMSSM12_MCMC1_45_795878.slha test/HSCPprod/data/.
cp /afs/desy.de/user/t/tlenz/HSCPworkdir/setup/setenvGENSIM/hscppythiapdt.tbl test/HSCPprod/data/.
echo "------------------------------------"
echo "--------------- Finished -----------"
echo "------------------------------------"
#cmsRun HSCPppstau_M_308_TuneZ2star_8TeV_pythia6_cff_py_GEN_SIM.py