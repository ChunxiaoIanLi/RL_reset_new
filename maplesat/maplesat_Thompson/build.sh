#!/bin/bash

# Modify the output filename with current timestamp
time=$(date +"%Y%m%d%H%M%S")
outputPath="./build/maplesat_static_$time"

# Build the project
make
mv ./core/maplesat_static $outputPath
echo $outputPath

# Append to the build history
echo $outputPath >> build_history.txt