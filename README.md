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
git clone <this_repo>
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
cd $OCSMEM_HOME/tpcds-kit/tools
make OS=LINUX CC=gcc-9
```

Create db and load schema
```
createdb tpcds
psql tpcds -f tpcds.sql
```

Change directory into DynamoRio build dir and generate data
```
cd $OCSMEM_HOME/dynamorio
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
