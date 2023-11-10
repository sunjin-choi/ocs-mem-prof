#!/usr/bin/env bash

echo "generate data and queries..."
cd $OCSPROF_HOME/workload
mkdir -p tpcds-query && cd tpcds-query

dsdgen -DISTRIBUTIONS $TPCDS_HOME/tools/tpcds.idx
dsqgen \
	-DIRECTORY $TPCDS_HOME/query_templates \
	-INPUT $TPCDS_HOME/query_templates/templates.lst \
	-VERBOSE Y \
	-QUALIFY Y \
	-SCALE 1 \
	-DIALECT netezza \
	-OUTPUT_DIR . \
	-DISTRIBUTIONS $TPCDS_HOME/tools/tpcds.idx

