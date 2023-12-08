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
if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <query_name> <scale> <rngseed> <tbl_size> <suffix> <mode>"
	echo "suffix is usually a machine name, but any designater will work"
    exit 1
fi

QUERY_NAME=$1
SCALE=$2
RNGSEED=$3
TBL_SIZE=$4
SUFFIX=$5
MODE=$6

## run dynamorio-elam
#cd build
#for QUERY_NAME in "${QUERY_NAMES[@]}"; do
#    echo "Running query: $QUERY_NAME"
#    CSV_FILE=/tmp/tpcds-trace/query_${QUERY_NAME}_scale_${SCALE}_rngseed_${RNGSEED}_${SUFFIX}.csv
#    ./bin64/drrun -t drcachesim --simulator_type elam -- bash ${OCSMEM_HOME}/script/run_query_prim.sh ${QUERY_NAME} ${SCALE} ${RNGSEED} 2> $CSV_FILE
#done

QUERY_TBL=catalog_sales

if [ "$MODE" == "debug" ]; then
	# run dynamorio-elam
	cd build
	echo "Running query: $QUERY_NAME"
	#./bin64/drrun -t drcachesim --simulator_type memsize -- bash ${OCSMEM_HOME}/script/run_query_prim.sh ${QUERY_NAME} ${SCALE} ${RNGSEED} ${TBL_SIZE} profile
else
	# run dynamorio-elam
	cd build
	echo "Running query: $QUERY_NAME"
	CSV_FILE=/tmp/db-ubmark-trace/query_${QUERY_NAME}_scale_${SCALE}_rngseed_${RNGSEED}_${QUERY_TBL}_ubmark_memsize_${TBL_SIZE}_${SUFFIX}.csv
	#./bin64/drrun -t drcachesim --simulator_type memsize -- bash ${OCSMEM_HOME}/script/run_query_prim.sh ${QUERY_NAME} ${SCALE} ${RNGSEED} ${TBL_SIZE} profile 2> $CSV_FILE
	./bin64/drrun -t drcachesim --simulator_type elam -- bash ${OCSMEM_HOME}/script/run_query_prim.sh ${QUERY_NAME} ${SCALE} ${RNGSEED} ${TBL_SIZE} profile 2> $CSV_FILE
fi
