#!/bin/bash                                                                    
#SBATCH --time=0-0:0:5300                                                      
#SBATCH --account=def-vganesh                                                  
#SBATCH --mem=10g                                                               

file=$1
build=$2
decay=$3

# ./core/maplesat_static -cpu-lim=5000 -reset-strategy=2 -reset-decay=$decay -reset-window-size=$window -rnd-init $1
# echo ./core/maplesat_static -cpu-lim=5000 -reset-frequency=$prob $1
#time $build -cpu-lim=5000 -reset-strategy=2 -reset-decay=$decay -rnd-init $file

time (timeout -s SIGINT 5000s $2 $1)
