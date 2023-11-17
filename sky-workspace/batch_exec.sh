#!/usr/bin/env bash

FILE="./sky-batch/instances.txt"

# Queries not working
# 2, 5, 12, 14, 16, 20, 21, 23
# Queries working
# ..., 17, 18, 19, 22, 24, 25, 26, 27, 28, 29, 30

while IFS= read -r line
do
	export QUERY_NUM=30
	sky exec sunjin-tpcds-$line -n Q${QUERY_NUM} --env QUERY_NUM=${QUERY_NUM} --env SCALE=1 --env RNGSEED=0 --env SUFFIX=$line ./sky-config/tpcds-query-profile.yml &
done < "$FILE"

#while IFS= read -r line
#do
#    sky exec sunjin-tpcds-$line --env QUERY_NUM=4 --env SCALE=1 --env RNGSEED=0 --env SUFFIX=$line ./sky-config/tpcds-query-profile.yml &
#done < "$FILE"
#
#
#while IFS= read -r line
#do
#    sky exec sunjin-tpcds-$line --env QUERY_NUM=4 --env SCALE=1 --env RNGSEED=0 --env SUFFIX=$line ./sky-config/tpcds-query-profile.yml &
#done < "$FILE"
