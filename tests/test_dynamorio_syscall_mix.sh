#!/usr/bin/env bash

export TEST_HOME=$OCSMEM_HOME/tests

cd $OCSMEM_HOME/build
./bin64/drrun -t drcachesim --simulator_type syscall_mix -- $TEST_HOME/memsyscall/syscall_getpid_100
