#!/usr/bin/env bash


sky launch -c sunjin-tpcds-prim-1 ./sky-config/setup/tpcds-setup-n2-standard-8.yml -i 20 -y -d &
sky launch -c sunjin-tpcds-prim-2 ./sky-config/setup/tpcds-setup-n2-standard-8.yml -i 20 -y -d &
#sky launch -c sunjin-tpcds-prim-test ./sky-config/setup/tpcds-setup-n2-standard-16.yml -i 20 -y -d &
