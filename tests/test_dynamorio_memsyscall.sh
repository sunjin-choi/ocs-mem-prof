#!/usr/bin/env bash

export TEST_HOME=$OCSMEM_HOME/tests

cd $OCSMEM_HOME/build
./bin64/drrun -t drcachesim --simulator_type memsyscall -- $TEST_HOME/memsyscall/syscall_mmap
