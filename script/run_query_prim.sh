#!/usr/bin/env bash

# Define the list of query names
declare -a QUERY_NAMES=(
	"distinct" \
	"full_scan" \
	"sort_order_by" \
	"single-column_aggregation_group_by_query" \
	"equijoin" \
	"range_scan" \
	"cross_join" \
)

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
	echo "Usage: $0 <query_name> <scale> <rngseed>"
	exit 1
fi

QUERY_NAME=$1
SCALE=$2
RNGSEED=$3

# Check if QUERY_NAME is in QUERY_NAMES array
if [[ ! " ${QUERY_NAMES[@]} " =~ " ${QUERY_NAME} " ]]; then
	echo "Invalid query name. Available queries are: ${QUERY_NAMES[*]}"
	exit 1
fi

## Check if the correct number of arguments are provided
#if [ "$#" -ne 2 ]; then
#    echo "Usage: $0 <scale> <rngseed>"
#    exit 1
#fi
#
#SCALE=$1
#RNGSEED=$2

DB_NAME=tpcds-scale-${SCALE}-rngseed-${RNGSEED}

psql $DB_NAME -f $OCSMEM_HOME/tpcds-query/${QUERY_NAME}_query.sql -P pager=off -o /dev/null
