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

## Check if the correct number of arguments are provided
#if [ "$#" -ne 1 ]; then
#    echo "Usage: $0 <query>"
#    echo "Available queries are: ${QUERY_NAMES[*]}"
#    exit 1
#fi
#
#QUERY_NAME=$1
#
## check if QUERY_NAME is in QUERY_NAMES
#if [[ ! " ${QUERY_NAMES[@]} " =~ " ${QUERY_NAME} " ]]; then
#    echo "Invalid query name. Available queries are: ${QUERY_NAMES[*]}"
#    exit 1
#fi

# loop over QUERY_NAMES while cluster name should be with incrementing index
#for i in "${!QUERY_NAMES[@]}"; do
#	QUERY_NAME=${QUERY_NAMES[$i]}
#	CLUSTER_NAME="sunjin-db-ubmark-${i}"
#
#	echo "Launching cluster ${CLUSTER_NAME}"
#	sky launch -c ${CLUSTER_NAME} \
#		-i 20 -y -d \
#		--env QUERY_NAME=${QUERY_NAME} \
#		--env SCALE=1 \
#		--env DATA_SUFFIX=_1_4 \
#		--env RNGSEED=0 \
#		--env TBL_SIZE=1000 \
#		--env CSV_SUFFIX=n2-standard-8 \
#		./sky-config/db_ubmark_runner/setup-and-run.yml \
#		&
#done

for i in "${!QUERY_NAMES[@]}"; do
	QUERY_NAME=${QUERY_NAMES[$i]}
	CLUSTER_NAME="sunjin-db-ubmark-${i}"

	echo "Running query ${QUERY_NAME} on cluster ${CLUSTER_NAME}"
	sky exec ${CLUSTER_NAME} \
		--env QUERY_NAME=${QUERY_NAME} \
		--env SCALE=1 \
		--env DATA_SUFFIX=_1_4 \
		--env RNGSEED=0 \
		--env TBL_SIZE=1000 \
		--env CSV_SUFFIX=n2-standard-8 \
		./sky-config/db_ubmark_runner/setup-and-run.yml \
		&
done

#sky exec sunjin-tpcds-prim -n $QUERY_NAME --env QUERY_NAME=$QUERY_NAME --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n1-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
##sky exec sunjin-tpcds-prim-test --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n2-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
