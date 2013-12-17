#!/bin/bash

cd results

for j in {100,200,300,400,500,600}; do 
    for i in {0..6}; do hadd pMSSM12_MCMC1_30_549144_m${j}_width${i}.root pMSSM12_MCMC1_30_549144_m${j}_width${i}_*.root; done
done

cd ..