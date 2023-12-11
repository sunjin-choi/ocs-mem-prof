# ocs-mem-prof

## Build instructions

First, install system dependencies (TODO: verify)
```
sudo apt-get install gcc make flex bison byacc git -y
sudo apt-get install gcc-9 build-essential cmake postgresql postgresql-client -y
```

Initialize postgresql
```
sudo -u postgres createuser --superuser $(whoami)
```

If you want to delete user or created database:
```
sudo -u postgres -c "dropuser <created_user>" # delete user
sudo -u postgres -c "dropdb <created_db>" # delete db
```

Initialize environment
```
git clone https://github.com/sunjin-choi/ocs-mem-prof/tree/master
git submodule update --init --recursive
chmod +x setup_path.sh
source setup_path.sh
```

Force postgress to only use one worker process (this makes instrumentation simpler)
```
echo "max_parallel_workers = 1" | sudo tee  -a /etc/postgresql/16/main/postgresql.conf
```

### DynamoRio
```
cd $OCSMEM_HOME/dynamorio
mkdir build
cd build
cmake ..
make -j
bin64/drrun -t drcachesim  -simulator_type elam -- ls
```

### TPC-DS kit
```
cd $OCSMEM_HOME/tpcds-kit/tools
make OS=LINUX CC=gcc-9
```

Create db and load schema
```
cd $OCSMEM_HOME/tpcds-kit/tools
createdb tpcds
psql tpcds -f tpcds.sql
```

Change directory into DynamoRio build dir and generate data
```
source setup_path.sh
cd $OCSMEM_HOME/dynamorio/build
./dsdgen -FORCE -VERBOSE
for i in `ls *.dat`; do
  table=${i/.dat/}
  echo "Loading $table..."
  sed 's/|$//' $i > /tmp/$i
  psql tpcds -q -c "TRUNCATE $table"
  psql tpcds -c "\\copy $table FROM '/tmp/$i' CSV DELIMITER '|'"
done
dsdgen -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx
```

Generate queries inside DynamoRio build dir
```
cd $OCSMEM_HOME/dynamorio/build
dsqgen -DIRECTORY $TPCHOME/query_templates -INPUT $TPCHOME/query_templates/templates.lst -VERBOSE Y -QUALIFY Y -SCALE 1 -DIALECT netezza -OUTPUT_DIR . -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx
```

Wrap psql query into bash: for two reasons, psql is a terminal wrapper which is a perl script and < does not look compatible with dynamorio
```
cd $OCSMEM_HOME/dynamorio/build
echo "perl /usr/bin/psql tpcds < query_0.sql" >> run_psql_query_0.sh
chmod +x run_psql_query_0.sh
./bin64/drrun -t drcachesim -simulator_type elam -- bash run_psql_query_0.sh 2> data.csv
```


## Data profiling

## Mounting Bucket with GCSFuse
install gcsfuse from https://cloud.google.com/storage/docs/gcsfuse-quickstart-mount-bucket
```
gcsfuse tpcds-trace bucket_data
```

## Run cache simulation
`bazel build //ocs_cache_sim:run_cache_sim`
`./run_cache_sim.sh [path_to_trace.csv]`
or run the binary directly (optionally writing a results csv with `-o`)
`./bazel-bin/ocs_cache_sim/run_cache_sim tests/fixture/two_pages.csv -n $( wc -l tests/fixture/two_pages.csv | awk '{print $1}') -o results.csv`

## Run Tests
`bazel test //ocs_cache_sim:basic_functionality_test`

## Update compile\_commands.json
`bazel run @hedron_compile_commands//:refresh_all`

## Set up and run mysql benchmark (full scan on an in-memory table)
`cd mysql; ./setup_script.sh`
`cd dynamorio/; echo "mysql -u test < '../mysql/bmark.sql'" > bmark_mysql.sh"`
`./bin64/drrun -t drcachesim -simulator_type elam -- bash bmark_mysql.sh 2> data.csv`

## Contiguous Access Example
`cd tests; g++ contrived_increasing_access.cpp`
`./bin64/drrun -t drcachesim -simulator_type elam -- ./a.out 2> data.csv`
It'll print out the base address


