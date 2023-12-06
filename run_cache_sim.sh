#!/bin/bash

# Check if exactly one argument (the filename) is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

# Count the number of lines in the file
line_count=$(wc -l < "$filename")

# Path to the hardcoded binary
binary="./bazel-bin/cache/run_cache_sim"

# Run the binary with the filename and line count as arguments
"$binary" "$filename" "$line_count"

