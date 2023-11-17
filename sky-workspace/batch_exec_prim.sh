#!/usr/bin/env bash

## Define the list of query names
#declare -a QUERY_NAMES=(
#    "single-column_aggregation_group_by" \
#    "equijoin" \
#    "range_scan" \
#    "cross_join" \
#    "distinct" \
#    "full_scan" \
#    "sort_order_by" \
#)
#
# Define the list of query names
declare -a QUERY_NAMES=(
    "cross_join" \
    "sort_order_by" \
)

# Loop through each query name and execute it
for i in "${!QUERY_NAMES[@]}"; do
    QUERY_NAME=${QUERY_NAMES[$i]}
    QUERY_INDEX=$((i + 1))  # Calculate the query index

    # Execute the query with the corresponding sunjin-tpcds-prim command
    sky exec sunjin-tpcds-prim-${QUERY_INDEX} -n $QUERY_NAME --env QUERY_NAME=$QUERY_NAME --env SCALE=1 --env RNGSEED=0 --env SUFFIX=n2-standard-8-limit-100 ./sky-config/tpcds-query-prim-profile.yml &
done
