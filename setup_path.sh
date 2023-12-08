#!/usr/bin/env bash

export OCSMEM_HOME=$PWD
export TPCHOME=$PWD/tpcds-kit
export DYNAMORIO_HOME=$PWD/dynamorio

export PATH=$PATH:$PWD/tpcds-kit/tools

export PYTHONPATH=$PYTHONPATH:$PWD/sky-workspace/sky_controller
