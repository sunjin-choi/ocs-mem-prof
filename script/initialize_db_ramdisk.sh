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
MODE=$5

DB_NAME=tpcds-scale-${SCALE}-rngseed-${RNGSEED}


# Set up variables
RAMDISK_DIR="/mnt/ramdisk"
RAMDISK_SIZE="10G"
DB_TABLESPACE="ramdisk_tablespace"

# Check if RAM disk is already mounted
if mount | grep -q "$RAMDISK_DIR"; then
    echo "RAM disk is already mounted."
else
    # Create and mount the RAM disk
    sudo mkdir -p $RAMDISK_DIR
    sudo mount -t tmpfs -o size=$RAMDISK_SIZE tmpfs $RAMDISK_DIR
    echo "RAM disk mounted at $RAMDISK_DIR."
fi

# Set permissions
sudo chown -R postgres:postgres $RAMDISK_DIR
sudo chmod 700 $RAMDISK_DIR

# Initialize database
cd $TPCHOME/tools
createdb $DB_NAME

# Create a tablespace on the RAM disk
psql $DB_NAME -c "CREATE TABLESPACE $DB_TABLESPACE LOCATION '$RAMDISK_DIR';"

# Set default tablespace to the RAM disk
psql $DB_NAME -c "ALTER DATABASE \"$DB_NAME\" SET default_tablespace = $DB_TABLESPACE;"

# Run the database schema setup script
psql $DB_NAME -f tpcds.sql

# Load data
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
    i=`ls catalog_sales${SUFFIX}.dat`
    table=${i/$SUFFIX.dat/}
    echo "Loading $table..."
    sed 's/|$//' $i > /tmp/$i
    psql $DB_NAME -q -c "TRUNCATE $table"
    psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
    psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_1000 AS SELECT * FROM catalog_sales ORDER BY RANDOM() LIMIT 1000;"

elif [ "$MODE" == "ubmark_5000" ]; then
    cd $DATA_DIR
    i=`ls catalog_sales${SUFFIX}.dat`
    table=${i/$SUFFIX.dat/}
    echo "Loading $table..."
    sed 's/|$//' $i > /tmp/$i
    psql $DB_NAME -q -c "TRUNCATE $table"
    psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
    psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_5000 AS SELECT * FROM catalog_sales ORDER BY RANDOM() LIMIT 5000;"

elif [ "$MODE" == "ubmark_10000" ]; then
	cd $DATA_DIR
	i=catalog_sales_1_4.dat
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_10000 AS SELECT * FROM catalog_sales ORDER BY RANDOM() LIMIT 10000;"

elif [ "$MODE" == "ubmark_50000" ]; then
	cd $DATA_DIR
	i=catalog_sales_1_4.dat
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_50000 AS SELECT * FROM catalog_sales ORDER BY RANDOM() LIMIT 50000;"

elif [ "$MODE" == "ubmark_100000" ]; then
	cd $DATA_DIR
	i=catalog_sales_1_4.dat
	table=${i/$SUFFIX.dat/}
	echo "Loading $table..."
	sed 's/|$//' $i > /tmp/$i
	psql $DB_NAME -q -c "TRUNCATE $table"
	psql $DB_NAME -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
	psql $DB_NAME -c "CREATE MATERIALIZED VIEW IF NOT EXISTS catalog_sales_ubmark_100000 AS SELECT * FROM catalog_sales ORDER BY RANDOM() LIMIT 100000;"

else
	echo "Invalid mode"
	exit 1
fi

## vacuum analyze
#psql $DB_NAME -c "VACUUM ANALYZE;"
