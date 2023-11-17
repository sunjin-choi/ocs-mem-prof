#!/usr/bin/env bash

# The first command line argument is stored in $1
COMMAND=$1

FILE="./sky-batch/instances.txt"

if [ "$COMMAND" = "launch" ]; then
    while IFS= read -r line
    do
        sky launch -c sunjin-tpcds-${line} ./sky-config/setup/tpcds-setup-${line}.yml -i 20 -y -d 2> ./logs/tpcds-setup-${line}.log &
    done < "$FILE"
elif [ "$COMMAND" = "down" ]; then
    while IFS= read -r line
    do
        sky down sunjin-tpcds-${line} -y &
    done < "$FILE"
elif [ "$COMMAND" = "start" ]; then
    while IFS= read -r line
    do
        sky start sunjin-tpcds-${line} -y &
    done < "$FILE"
elif [ "$COMMAND" = "cancel" ]; then
    while IFS= read -r line
    do
        sky cancel sunjin-tpcds-${line} -a -y &
    done < "$FILE"
elif [ "$COMMAND" = "autostop" ]; then
    while IFS= read -r line
    do
        sky autostop sunjin-tpcds-${line} -i 30 -y &
    done < "$FILE"
elif [ "$COMMAND" = "mount" ]; then
    while IFS= read -r line
    do
        sky launch --no-setup -c sunjin-tpcds-${line} ./sky-config/setup/tpcds-setup-${line}.yml -i 20 -y -d 2> ./logs/tpcds-setup-${line}.log &
    done < "$FILE"


else
    echo "Invalid command. Usage: $0 launch"
fi
