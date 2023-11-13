#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <dump_path> <scale> <rngseed>"
    exit 1
fi

DUMP_PATH=$1
SCALE=$2
RNGSEED=$3

echo "generate data in ${1}"
mkdir -p $DUMP_PATH

echo "data generation with scale ${2} and rngseed ${3}"

dsdgen \
    -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx \
    -VERBOSE Y \
	-PARALLEL 4 \
    -FORCE \
	-DIR $DUMP_PATH \
    -SCALE $SCALE \
	-RNGSEED $RNGSEED

