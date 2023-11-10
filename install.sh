#!/usr/bin/env bash

echo "initialize postgres..."
sudo su postgres -c "createuser $(whoami) --superuser"

echo "build tpc-ds tool..."
cd $TPCDS_HOME
make OS=LINUX CC=gcc-9

createdb tpcds
psql tpcds -f tpcds.sql

echo "build dynamorio..."
cd $DYNAMORIO_HOME
mkdir build && cd build
cmake --configure ..
cmake .
make -j
