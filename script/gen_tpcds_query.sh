#!/usr/bin/env bash

QUERY_DIRECTORY=/tmp/tpcds-query

mkdir -p $QUERY_DIRECTORY

for i in {1..99}; do
    # Construct the query file name
    query_tpl_file="query${i}.tpl"

    # Append the query file name to itself (if that's what you really want to do)
    echo $query_tpl_file >> $query_tpl_file

    # Execute dsqgen with the dynamically generated query file name
    dsqgen \
        -DIRECTORY $TPCHOME/query_templates \
        -INPUT $query_tpl_file \
        -VERBOSE Y \
        -QUALIFY Y \
        -SCALE 1 \
        -DIALECT netezza \
        -OUTPUT_DIR $QUERY_DIRECTORY \
        -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx

	cp $QUERY_DIRECTORY/query_0.sql $QUERY_DIRECTORY/query_${i}.sql

done

# Final dsqgen outputs query_0.sql
dsqgen \
	-DIRECTORY $TPCHOME/query_templates \
	-INPUT $TPCHOME/query_templates/templates.lst \
	-VERBOSE Y \
	-QUALIFY Y \
	-SCALE 1 \
	-DIALECT netezza \
	-OUTPUT_DIR $QUERY_DIRECTORY \
	-DISTRIBUTIONS $TPCHOME/tools/tpcds.idx

