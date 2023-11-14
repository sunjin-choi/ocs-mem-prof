#!/usr/bin/env bash

echo "initialize postgres..."
sudo su postgres -c "createuser $(whoami) --superuser"

echo "build dynamorio..."
cd $OCSMEM_HOME
mkdir build
cd build
cmake --configure $DYNAMORIO_HOME
cmake .
make -j
