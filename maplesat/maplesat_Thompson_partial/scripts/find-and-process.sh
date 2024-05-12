#!/bin/bash

inputDir=$1
inputRegex=$2
outputDir=$3
outputPrefix=$4

if [ -z "$inputDir" ] || [ -z "$inputRegex" ]
then
	echo "Usage: ./find-and-process.sh INPUT-DIR INPUT-REGEX"
	exit
fi

for filepath in $inputDir/$inputRegex; do
    # echo $filename
    # filename="$(basename -- $filepath)"

    echo $filepath
    python3 process-reset-stats.py $filepath
done