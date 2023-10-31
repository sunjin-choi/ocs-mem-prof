# ocs-mem-prof

## Build instructions

First, install system dependencies (TODO: verify)
```
sudo apt-get install gcc make flex bison byacc git 
sudo apt-get install gcc-9 build-essential cmake postgres
```

Initialize postgresql
```
sudo -u postgres createuser -s $(whoami); createdb $(whoami)
```

### DynamoRio
```
cd dynamorio
mkdir build
cd build
cmake --configure ..
cmake .
make
bin64/drrun -t drcachesim  -simulator_type elam -- ls
```

### TPC-DS kit
```
cd tpcds-kit/tools
make OS=LINUX
```

Create db and load schema
```
createdb tpcds
psql tpcds -f tpcds.sql
```

Change directory into DynamoRio build dir and generate data
```
cd <dynamo_build_dir>
dsdgen -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx
```

Generate queries inside DynamoRio build dir
```
dsqgen -DIRECTORY $TPCHOME/query_templates -INPUT $TPCHOME/query_templates/templates.lst -VERBOSE Y -QUALIFY Y -SCALE 1 -DIALECT netezza -OUTPUT_DIR . -DISTRIBUTIONS $TPCHOME/tools/tpcds.idx
```

Wrap psql query into bash: for two reasons, psql is a terminal wrapper which is a perl script and < does not look compatible with dynamorio
```
echo "perl /usr/bin/psql tpcds < query_0.sql" >> run_psql_query_0.sh
chmod +x run_psql_query_0.sh
./bin64/drrun -t drcachesim -simulator_type elam -- bash run_psql_query_0.sh 2> data.csv
```


## Data profiling
