#!/usr/bin/env bash


# Define the list of query names
declare -a QUERY_NAMES=(
	"single-column_aggregation_group_by" \
	"equijoin" \
	"range_scan" \
	"cross_join" \
	"distinct" \
	"full_scan" \
	"sort_order_by" \
)

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <query>"
	echo "Available queries are: ${QUERY_NAMES[*]}"
    exit 1
fi

QUERY_NAME=$1

# check if QUERY_NAME is in QUERY_NAMES
if [[ ! " ${QUERY_NAMES[@]} " =~ " ${QUERY_NAME} " ]]; then
	echo "Invalid query name. Available queries are: ${QUERY_NAMES[*]}"
	exit 1
fi

sky exec sunjin-tpcds-prim -n $QUERY_NAME --env QUERY_NAME=$QUERY_NAME --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n1-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
#sky exec sunjin-tpcds-prim-test --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n2-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
