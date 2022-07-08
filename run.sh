#!/usr/bin/env bash

source activate ibm

# parameters
sims=1000
t=1000
tr=0.0
C=1
des="env_stoch 4:1, stoch dorm, one cell type"

# setup output directory
dt=$(date "+%Y%m%d_%H%M")
sourcepath=$(pwd)
python=$sourcepath/python
output=$sourcepath/output/${dt}_${sims}sims_t${t}
log=$output/log_file.txt

# remove output directory if it exists
if [ -d $output ]; then rm -r $output; fi

mkdir $output

# initialize log file
touch $log

# run sim
time python $python/main.py -S $sims -t $t -o $output/ -tr $tr -C $C -R -es -des "$des" > $log

