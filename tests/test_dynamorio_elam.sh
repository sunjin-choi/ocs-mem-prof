#!/usr/bin/env bash

export TEST_HOME=$OCSMEM_HOME/tests

MODE=$1

cd $OCSMEM_HOME/build
if [ "$MODE" = "debug" ]; then
	./bin64/drrun -t drcachesim --simulator_type elam -- ls
elif [ "$MODE" = "generate" ]; then
	./bin64/drrun -t drcachesim --simulator_type elam -- ls 2> $TEST_HOME/test_ls.csv
else
	echo "Usage: test_dynamorio_elam.sh [debug/generate]"
fi
