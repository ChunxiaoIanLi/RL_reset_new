#!/bin/bash                                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh                                                  
#SBATCH --mem=10g                                                               

file=$1
build=$2
decay=$3

SBVA=./sbva

OUTER_TIMEOUT=400
INNER_TIMEOUT=200

time (timeout -s SIGINT 5000s python3 wrapper.py \
    --input $1 \
    --output $2 \
    --bva $SBVA \
    --t1 $INNER_TIMEOUT \
    --t2 $OUTER_TIMEOUT \
    --solver $build)
