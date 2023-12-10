import mysql.connector
from tqdm import tqdm


# Connect to MySQL
conn = mysql.connector.connect(
  host="localhost",
  user="test",
  database="test_db"
)
cursor = conn.cursor()

print("Inserting 1,000,000 rows...")
for i in tqdm(range(1000000)):
    query = "INSERT INTO test_in_memory_table (name) VALUES (%s)"
    values = (f"value1_{i}",)
    cursor.execute(query, values)

# Commit and close
conn.commit()
cursor.close()
conn.close()

