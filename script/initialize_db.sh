#!/usr/bin/env bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <path-to-data-dir> <suffix> <scale> <rngseed>"
	echo "Initializes postgres db with tpcds and loads data from data directory with suffix"
    exit 1
fi

DATA_DIR=$1
SUFFIX=$2
SCALE=$3
RNGSEED=$4

DB_NAME=tpcds-scale-${SCALE}-rngseed-${RNGSEED}

# initialize db
cd $TPCHOME/tools
createdb $DB_NAME
psql $DB_NAME -f tpcds.sql

# load data
cd $DATA_DIR
for i in `ls *${SUFFIX}.dat`; do
  table=${i/$SUFFIX.dat/}
  echo "Loading $table..."
  sed 's/|$//' $i > /tmp/$i
  psql $DB_NAME -q -c "TRUNCATE $table"
  psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
done
