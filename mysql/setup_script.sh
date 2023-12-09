#!/bin/bash
sudo mysql -u root < perm_setup.sql
mysql -u test < in_memory_table_creation.sql
python3 populate_table.py
