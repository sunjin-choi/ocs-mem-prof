#!/usr/bin/env bash

echo "initialize postgres..."
sudo su postgres -c "createuser $(whoami) --superuser"

echo "build tpc-ds tool..."
cd $TPCDS_HOME/tools
make OS=LINUX CC=gcc-9

echo "build dynamorio..."
cd $OCSMEM_HOME
mkdir build && cd build
cmake --configure $DYNAMORIO_HOME
cmake .
make -j
