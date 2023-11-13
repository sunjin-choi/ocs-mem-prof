#!/usr/bin/env bash

echo "build tpc-ds tool..."
cd $TPCDS_HOME/tools
make OS=LINUX CC=gcc-9
