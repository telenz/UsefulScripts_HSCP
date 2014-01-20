#!/bin/bash

for j in {200,300,400,500,700,800}; do 
    for i in {0..14}; do  
	find save/*  -name "pMSSM12_MCMC1_30_549144_m${j}_width${i}_*" > filelist.txt
	sed -i -e 's/^/file:/' filelist.txt
	edmCopyPickMerge inputFiles_load=filelist.txt outputFile=file:results/pMSSM12_MCMC1_30_549144_m${j}_width${i}.root
    done
done 



