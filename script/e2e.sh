#!/usr/bin/env bash

cd $TPCHOME/tools
createdb tpcds
psql tpcds -f tpcds.sql

echo "generate data and queries..."
cd $OCSMEM_HOME/workload
mkdir -p tpcds-query && cd tpcds-query

dsdgen \
	-DISTRIBUTIONS $TPCHOME/tools/tpcds.idx \
	-VERBOSE Y \
	-FORCE \
	-SCALE 1

for i in `ls *.dat`; do
  table=${i/.dat/}
  echo "Loading $table..."
  sed 's/|$//' $i > /tmp/$i
  psql tpcds -q -c "TRUNCATE $table"
  psql tpcds -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
done

dsqgen \
	-DIRECTORY $TPCHOME/query_templates \
	-INPUT $TPCHOME/query_templates/templates.lst \
	-VERBOSE Y \
	-QUALIFY Y \
	-SCALE 1 \
	-DIALECT netezza \
	-OUTPUT_DIR . \
	-DISTRIBUTIONS $TPCHOME/tools/tpcds.idx

