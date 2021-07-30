#!/usr/bin/env bash

source activate ibm

sourcepath=$(pwd)
python=$sourcepath/python

dt=$(date "+%Y%m%d_%H%M")

# parameters
sims=1000
t=1000
tr=0
C=1


output=$sourcepath/output/${dt}_${sims}sims_t${t}
log=$output/log_file.txt

# remove output directory if it exists
if [ -d $output ]; then rm -r $output; fi

mkdir $output

# initialize log file
touch $log

time python $python/main.py -S $sims -t $t -tr $tr -o $output/ -R -C $C -es > $log

