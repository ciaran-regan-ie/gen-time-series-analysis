#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <FILENAME>"
  exit 1
fi

# Extract the file name without the extension
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"

# Define the path to the data directory and the file
DATA_DIR="src/data"
FILE_PATH="$DATA_DIR/$filename.$extension"

# Run the Julia script with the specified arguments
julia src/pipeline.jl "$FILE_PATH" lightweight --n-test 20 --iters 5 --epochs 200 --sched constant --shortname "$filename" --chains 1
