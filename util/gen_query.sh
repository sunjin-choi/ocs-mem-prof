#!/usr/bin/env bash

echo "generate data and queries..."
cd $DYNAMORIO_HOME/build
mkdir -p tpcds-query && cd tpcds-query

dsdgen -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx
dsqgen \
	-DIRECTORY $TPCHOME/query_templates \
	-INPUT $TPCHOME/query_templates/templates.lst \
	-VERBOSE Y \
	-QUALIFY Y \
	-SCALE 1 \
	-DIALECT netezza \
	-OUTPUT_DIR . \
	-DISTRIBUTIONS $TPCHOME/tools/tpcds.idx

