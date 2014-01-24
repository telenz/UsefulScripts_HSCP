#!/bin/bash

# 1.) Set up a cmssw are (CMMSW_5_3_2_patch4 or CMSSW_5_3_X)
# 2.) copy that sript in source folder and run it with source setupAnalysis

# The script checks out "TheNtupleMaker" and initialize it
if [ -d "PhysicsTools" ]; then
    cd PhysicsTools
    echo "PhysicsTools already exists."
else
    mkdir PhysicsTools
    cd PhysicsTools
fi
git clone https://github.com/hbprosper/TheNtupleMaker.git
cd TheNtupleMaker
cmsenv
scripts/initTNM.py
scram b clean
scram b -j8

# Then it checks out the analysis code 
cd ../..
git clone https://github.com/telenz/Ntuples.git
cmsenv
scram b -j8
echo
echo "------------------------------------------"
echo "------- Initialization finished ----------"
echo "------------------------------------------"