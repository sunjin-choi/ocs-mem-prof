CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;

DROP TABLE IF EXISTS test_in_memory_table;

CREATE TABLE test_in_memory_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=MEMORY;

INSERT INTO test_in_memory_table (name) VALUES ('Example Name');
SELECT * FROM test_in_memory_table;

