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

psql $DB_NAME -f $OCSMEM_HOME/tpcds-query/query_${QUERY_NUM}.sql -P pager=off -o /dev/null

