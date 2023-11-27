#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <query_num> <scale> <rngseed>"
    exit 1
fi

QUERY_NUM=$1
SCALE=$2
RNGSEED=$3

DB_NAME=tpcds-scale-${SCALE}-rngseed-${RNGSEED}
QUERY_DIR=${OCSMEM_HOME}/benchmark/db_tpcds_query
QUERY_FILE=${QUERY_DIR}/query_${QUERY_NUM}.sql

psql $DB_NAME -f ${QUERY_FILE} -P pager=off -o /dev/null

