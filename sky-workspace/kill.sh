#!/bin/bash

# Get the list of defunct python3 processes and their parent process IDs
defunct_processes=$(ps -ef | grep 'python3' | grep 'defunct' | awk '{print $3}')

# Kill the parent processes of the defunct python3 processes
for ppid in $defunct_processes
do
    echo "Killing parent process: $ppid"
    kill -9 $ppid
done

