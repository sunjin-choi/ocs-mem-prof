#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <query_num> <scale> <rngseed> <suffix>"
	echo "suffix is usually a machine name, but any designater will work"
    exit 1
fi

QUERY_NUM=$1
SCALE=$2
RNGSEED=$3
SUFFIX=$4

CSV_FILE=/tmp/tpcds-trace/query_${QUERY_NUM}_scale_${SCALE}_rngseed_${RNGSEED}_${SUFFIX}.csv

# setup tmp dir
mkdir -p /tmp/tpcds-trace

# run dynamorio-elam
cd build
./bin64/drrun -t drcachesim --simulator_type elam -- bash ${OCSMEM_HOME}/script/run_query.sh ${QUERY_NUM} ${SCALE} ${RNGSEED} 2> $CSV_FILE
