#!/usr/bin/env bash

# Define the list of query names
declare -a QUERY_NAMES=(
	"distinct" \
	"full_scan" \
	"sort_order_by" \
	#"single-column_aggregation_group_by_query" \
	#"equijoin" \
	#"range_scan" \
	#"cross_join" \
)

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <scale> <rngseed> <suffix>"
	echo "suffix is usually a machine name, but any designater will work"
    exit 1
fi

SCALE=$1
RNGSEED=$2
SUFFIX=$3

# run dynamorio-elam
cd build
for QUERY_NAME in "${QUERY_NAMES[@]}"; do
	echo "Running query: $QUERY_NAME"
	CSV_FILE=/tmp/tpcds-trace/query_${QUERY_NAME}_scale_${SCALE}_rngseed_${RNGSEED}_${SUFFIX}.csv
	./bin64/drrun -t drcachesim --simulator_type elam -- bash ${OCSMEM_HOME}/script/run_query_prim.sh ${QUERY_NAME} ${SCALE} ${RNGSEED} 2> $CSV_FILE
done

