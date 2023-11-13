#!/usr/bin/env bash

mkdir -p /tmp/tpcds-query

echo “query_1.tpl” >> query_1.tpl

dsqgen \
	-DIRECTORY $TPCHOME/query_templates \
	-INPUT query_1.tpl \
	-VERBOSE Y \
	-QUALIFY Y \
	-SCALE 1 \
	-DIALECT netezza \
	-OUTPUT_DIR /tmp/tpcds-query \
	-DISTRIBUTIONS $TPCHOME/tools/tpcds.idx

