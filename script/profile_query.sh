#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <query_num> <scale> <rngseed>"
    exit 1
fi

QUERY_NUM=$1
SCALE=$2
RNGSEED=$3

# run dynamorio-elam
cd build
./bin64/drrun -t drcachesim --simulator_type elam -- bash run_query.sh ${QUERY_NUM} ${SCALE} ${RNGSEED}
