#!/usr/bin/env bash

echo "build tpc-ds tool..."
cd $TPCHOME/tools
make OS=LINUX CC=gcc-9
