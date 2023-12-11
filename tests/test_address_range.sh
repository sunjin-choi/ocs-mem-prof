#!/usr/bin/env bash

SUFFIX=$1

# if no suffix is provided, error out
if [ -z "$SUFFIX" ]; then
	echo "Usage: ./test_address_range.sh <suffix>"
	exit 1
fi

# setup array
declare -a VALIDATION_BINARIES=(
	"stack_access" \
	"heap_access" \
	#"contrived_increasing_access" \
)	

for VAL in "${VALIDATION_BINARIES[@]}"; do	
	CSV_FILE=/tmp/db-ubmark-trace/test_${VAL}_${SUFFIX}.csv

	# run dynamorio-elam
	cd ${OCSMEM_HOME}/build
	./bin64/drrun -t drcachesim --simulator_type elam -- ${OCSMEM_HOME}/tests/tracegen/${VAL} 2> ${CSV_FILE}
done
