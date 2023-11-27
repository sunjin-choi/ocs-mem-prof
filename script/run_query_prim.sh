#!/usr/bin/env bash

# Define the list of query names
declare -a QUERY_NAMES=(
	"distinct" \
	"full_scan" \
	"sort_order_by" \
	"single-column_aggregation_group_by" \
	"equijoin" \
	"range_scan" \
	"cross_join" \
	"all" \
)

# Check if the correct number of arguments are provided
if [ "$#" -ne 5 ]; then
	echo "Usage: $0 <query_name> <scale> <rngseed> <tbl_size> <mode>"
	exit 1
fi

QUERY_NAME=$1
SCALE=$2
RNGSEED=$3
TBL_SIZE=$4
MODE=$5

# Check if QUERY_NAME is in QUERY_NAMES array
if [[ ! " ${QUERY_NAMES[@]} " =~ " ${QUERY_NAME} " ]]; then
	echo "Invalid query name. Available queries are: ${QUERY_NAMES[*]}"
	exit 1
fi

DB_NAME=tpcds-scale-${SCALE}-rngseed-${RNGSEED}
QUERY_DIR=${OCSMEM_HOME}/benchmark/db_ubmark_query
QUERY_TBL=catalog_sales
QUERY_FILE=${QUERY_DIR}/${QUERY_NAME}_${QUERY_TBL}_ubmark_${TBL_SIZE}_query.sql

# if MODE is debug, then print to stdout
if [ "$MODE" == "debug" ]; then
	psql $DB_NAME -f ${QUERY_FILE} -P pager=off
else
	psql $DB_NAME -f ${QUERY_FILE} -P pager=off -o /dev/null
fi
