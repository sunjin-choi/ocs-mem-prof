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

declare -a TBL_SIZES=(
	1000 \
	10000 \
	100000 \
)

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <mode>"
	echo "Available modes are setup and run"
    exit 1
fi

MODE=$1

#QUERY_NAME=$1
#
## check if QUERY_NAME is in QUERY_NAMES
#if [[ ! " ${QUERY_NAMES[@]} " =~ " ${QUERY_NAME} " ]]; then
#    echo "Invalid query name. Available queries are: ${QUERY_NAMES[*]}"
#    exit 1
#fi

if [ "$MODE" = "setup" ]; then

for tbl_size in "${TBL_SIZES[@]}"; do	
	# loop over QUERY_NAMES while cluster name should be with incrementing index
	for i in "${!QUERY_NAMES[@]}"; do
		QUERY_NAME=${QUERY_NAMES[$i]}
		CLUSTER_NAME="sunjin-db-ubmark-${i}-${tbl_size}"

		echo "Launching cluster ${CLUSTER_NAME}"
		sky launch -c ${CLUSTER_NAME} \
			-i 10 --down -y -d \
			--env QUERY_NAME=${QUERY_NAME} \
			--env SCALE=1 \
			--env DATA_SUFFIX=_1_4 \
			--env RNGSEED=0 \
			--env TBL_SIZE=${tbl_size}\
			--env CSV_SUFFIX=n2-standard-16 \
			./sky-config/db_ubmark_runner/setup.yml \
			&
	done
done 

elif [ "$MODE" = "run" ]; then

for tbl_size in "${TBL_SIZES[@]}"; do	
	for i in "${!QUERY_NAMES[@]}"; do
		QUERY_NAME=${QUERY_NAMES[$i]}
		CLUSTER_NAME="sunjin-db-ubmark-${i}-${tbl_size}"

		echo "Running query ${QUERY_NAME} on cluster ${CLUSTER_NAME}"
		sky exec ${CLUSTER_NAME} \
			-n ${QUERY_NAME}_${tbl_size} \
			--env QUERY_NAME=${QUERY_NAME} \
			--env SCALE=1 \
			--env DATA_SUFFIX=_1_4 \
			--env RNGSEED=0 \
			--env TBL_SIZE=${tbl_size}\
			--env CSV_SUFFIX=n2-standard-16 \
			./sky-config/db_ubmark_runner/run.yml \
			&
	done
done 

elif [ "$MODE" = "down" ]; then

for i in "${!QUERY_NAMES[@]}"; do
	QUERY_NAME=${QUERY_NAMES[$i]}
	CLUSTER_NAME="sunjin-db-ubmark-${i}"

	sky down ${CLUSTER_NAME} -y &
done

fi

#sky exec sunjin-tpcds-prim -n $QUERY_NAME --env QUERY_NAME=$QUERY_NAME --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n1-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
##sky exec sunjin-tpcds-prim-test --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n2-standard-8 ./sky-config/tpcds-query-prim-profile.yml &
