
# Dictionary mapping descriptive strings to SQL queries
tpc_ds_queries = {
    "Full Scan": "SELECT * FROM {table} WHERE {column} IS NOT NULL;",
    "Cross Join": "SELECT * FROM {table} A CROSS JOIN {alt_table} B;",
    "Equijoin": "SELECT * FROM {table} JOIN {alt_table} ON {table}.{join_column} = {alt_table}.{alt_join_column};",
    "Range Scan": "SELECT * FROM {table} WHERE {range_column} BETWEEN {value_1} AND {value_2};",
    "DISTINCT": "SELECT DISTINCT {column} FROM {table};",
    "Single-Column Aggregation (GROUP BY)": "SELECT {column}, COUNT(*) FROM {table} GROUP BY {group_column};",
    "Sort (ORDER BY)": "SELECT * FROM {table} NATURAL JOIN {dates_table} ORDER BY {order_column};",
}

# Constants representing table and column names
sales_tbl = "catalog_sales"
items_tbl = "item"
dates_tbl = "date_dim"
order_column = "cs_wholesale_cost"
group_column = "cs_bill_customer_sk"
sales_col = "cs_item_sk"
join_col = "i_item_sk"
range_col = "d_year"
range_from = 1999
range_to = 2003

def save_query_to_file(query, filename):
    with open(filename, 'w') as file:
        file.write(query)

# Generate and save queries
for query_name, template in tpc_ds_queries.items():
    query = template.format(table=sales_tbl, column=sales_col, alt_table=items_tbl,
                            join_column=join_col, alt_join_column=join_col,
                            range_column=range_col, value_1=range_from, value_2=range_to,
                            group_column=group_column, dates_table=dates_tbl, order_column=order_column)
    
    filename = f"{query_name.replace(' ', '_').lower()}_query.sql"
    save_query_to_file(query, filename)
    print(f"Saved query '{query_name}' to file '{filename}'")
