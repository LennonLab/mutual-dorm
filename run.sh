#!/usr/bin/env bash

source activate ibm

sourcepath=$(pwd)
python=$sourcepath/python

dt=$(date "+%Y%d%m_%H%M")
sims=100
t=100

output=$sourcepath/output/${dt}_${sims}sims_t${t}

time python $python/main.py -S $sims -t $t -o $output

