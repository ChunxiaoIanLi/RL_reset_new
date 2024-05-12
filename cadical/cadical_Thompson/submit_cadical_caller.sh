#!/bin/bash                                                                    
#SBATCH --time=1-0:0:5300                                                      
#SBATCH --account=def-vganesh                                                  
#SBATCH --mem=10g                                                               

path=$1
build=$2
decay=$3
suffix=$4

# Sanity check for empty string
if [ -z "$path" ] || [ -z "$build" ] || [ -z "$decay" ] || [ -z "$suffix" ]
then
	echo "Usage: ./submit_maplesat_caller.sh <Path> <Build> <Decay> <Suffix>"
	exit 1
fi

# Check if path is an existing directory
if [ ! -d "$path" ] 
then
    echo "Directory $path DOES NOT exist." 
    exit 1
fi

# Check if build is an existing file
if [ ! -f "$build" ]; then
    echo "$build DOES NOT exist."
    exit 1
fi

# Check if decay is a number
re='^[+-]?[0-9]+\.?[0-9]*$'
if ! [[ $decay =~ $re ]] ; then
   echo "Error: The decay is not a number." 
   exit 1
fi

for i in $(find $path -name "*.cnf"); do 
    sbatch -o $i.$suffix.cadicalreset.log submit_cadical.sh $i $build $decay; 
done
