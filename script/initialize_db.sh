#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <path-to-data-dir> <suffix> <scale> <rngseed> <mode>"
	echo "Initializes postgres db with tpcds and loads data from data directory with suffix"
	echo "mode is either tpcds, ubmark_1000, ubmark_10000, ubmark_100000"
	echo "scale and rngseed correspond to those used to generate tpcds data"
	echo "at ubmark mode, data is subsampled"
    exit 1
fi

declare -a MODES=(
	"tpcds" \
	"ubmark_1000" \
	"ubmark_10000" \
	"ubmark_100000" \
)

DATA_DIR=$1
SUFFIX=$2
SCALE=$3
RNGSEED=$4
#MODE=$5

DB_NAME=${MODE}-scale-${SCALE}-rngseed-${RNGSEED}

# initialize db
cd $TPCHOME/tools
createdb $DB_NAME
psql $DB_NAME -f tpcds.sql

# load data
if [ "$MODE" == "tpcds" ]; then
	cd $DATA_DIR
	for i in `ls *${SUFFIX}.dat`; do
		table=${i/$SUFFIX.dat/}
		echo "Loading $table..."
		sed 's/|$//' $i > /tmp/$i
		psql $DB_NAME -q -c "TRUNCATE $table"
		psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	done

elif [ "$MODE" == "ubmark_1000" ]; then
	cd $DATA_DIR
	SUFFIX=catalog_sales_1_4
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_1000 AS SELECT * FROM catalog_sales LIMIT 1000;"

elif [ "$MODE" == "ubmark_10000" ]; then
	cd $DATA_DIR
	SUFFIX=catalog_sales_1_4
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_10000 AS SELECT * FROM catalog_sales LIMIT 10000;"

elif [ "$MODE" == "ubmark_100000" ]; then
	cd $DATA_DIR
	SUFFIX=catalog_sales_1_4
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_100000 AS SELECT * FROM catalog_sales LIMIT 100000;"

else
	echo "Invalid mode"
	exit 1
fi

# vacuum analyze
psql $DB_NAME -c "VACUUM ANALYZE;"


