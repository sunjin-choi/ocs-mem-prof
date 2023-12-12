#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <query_num> <scale> <rngseed> <suffix> <num_samples>"
	echo "suffix is usually a machine name, but any designater will work"
    exit 1
fi

QUERY_NUM=$1
SCALE=$2
RNGSEED=$3
SUFFIX=$4
NUM_SAMPLES=$5

CSV_FILE=/tmp/tpcds-trace/query_${QUERY_NUM}_scale_${SCALE}_rngseed_${RNGSEED}_${SUFFIX}.csv

# run dynamorio-elam
cd ${OCSMEM_HOME}
./run_cache_sim.sh $CSV_FILE $NUM_SAMPLES
