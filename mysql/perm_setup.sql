CREATE DATABASE IF NOT EXISTS test_db;
CREATE USER IF NOT EXISTS 'test'@'localhost';
GRANT ALL PRIVILEGES on test_db.* TO  'test'@'localhost';

SET GLOBAL tmp_table_size = 1024 * 1024 * 1024 * 10;
SET GLOBAL max_heap_table_size = 1024 * 1024 * 1024 * 11;
