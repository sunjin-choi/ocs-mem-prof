#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <dump_path> <scale>"
    exit 1
fi

DUMP_PATH=$1
SCALE=$2

echo "generate data in ${1}"
mkdir -p $DUMP_PATH && cd $DUMP_PATH

dsdgen \
    -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx \
    -VERBOSE Y \
    -FORCE \
    -SCALE $SCALE
