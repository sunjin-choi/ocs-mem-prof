#!/bin/bash

# Check if exactly one argument (the filename) is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename> <sim_first_n_lines>"
	echo "To run all, sim_first_n_lines = -1"
    exit 1
fi

filename=$1
sim_first_n_lines=$2

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi
 
# Extract the base name of the file without the extension
base_name=$(basename "$filename" | cut -d. -f1)

# Output file name with 'ocs' prefix and .csv extension
output_file="$(dirname "$filename")/ocs_${base_name}.csv"

# Count the number of lines in the file
line_count=$(wc -l < "$filename")
line_count=$(wc -l "$filename" | awk '{print $1}')

# Path to the hardcoded binary
binary="./bazel-bin/ocs_cache_sim/run_cache_sim"

# Run the binary with the filename and line count as arguments
"$binary" "$filename" -n "$line_count" -o "$output_file" --sim_first_n_lines "$sim_first_n_lines"
#"$binary" "$filename" -n "$line_count" -o "$output_file" -v
