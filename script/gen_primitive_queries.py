
# Dictionary mapping descriptive strings to SQL queries
# TODO indices might have an optimization where even if it's a reference you can read the actual column value directly out of the index and thus avoid ios int
tpc_ds_queries = {
    "Full Scan": "SELECT * FROM {table} WHERE {column} IS NOT NULL;",
    "Cross Join": "SELECT * FROM {table} A CROSS JOIN {alt_table} B;",
    "Equijoin": "SELECT * FROM {table} JOIN {alt_table} ON {table}.{join_column} = {alt_table}.{alt_join_column};",
    # "Range Scan": "SELECT * FROM {table} NATURAL JOIN {dates_table} WHERE {range_column} BETWEEN {value_1} AND {value_2};",
    "Range Scan": "SELECT * FROM {table} WHERE {range_column} BETWEEN {value_1} AND {value_2};",
    "DISTINCT": "SELECT DISTINCT {column} FROM {table};",
    "Single-Column Aggregation (GROUP BY)": "SELECT {group_column}, COUNT(*) FROM {table} GROUP BY {group_column};",
    # "Sort (ORDER BY)": "SELECT * FROM {table} NATURAL JOIN {dates_table} ORDER BY {order_column};",
    "Sort (ORDER BY)": "SELECT * FROM {table} ORDER BY {order_column};",
}

# tpc_ds_queries = {
#     "Full Scan": """
#         SELECT *
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         WHERE {column} IS NOT NULL;
#     """,
#
#     "Cross Join": """
#         SELECT *
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         CROSS JOIN (SELECT * FROM {alt_table} LIMIT {limit}) AS sub_{alt_table};
#     """,
#
#     "Equijoin": """
#         SELECT *
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         JOIN (SELECT * FROM {alt_table} LIMIT {limit}) AS sub_{alt_table}
#         ON sub_{table}.{join_column} = sub_{alt_table}.{alt_join_column};
#     """,
#
#     "Range Scan": """
#         SELECT *
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         NATURAL JOIN (SELECT * FROM {dates_table} LIMIT {limit}) AS sub_{dates_table}
#         WHERE {range_column} BETWEEN {value_1} AND {value_2};
#     """,
#
#     "DISTINCT": """
#         SELECT DISTINCT {column}
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table};
#     """,
#
#     "Single-Column Aggregation (GROUP BY)": """
#         SELECT {group_column}, COUNT(*)
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         GROUP BY {group_column};
#     """,
#
#     "Sort (ORDER BY)": """
#         SELECT *
#         FROM (SELECT * FROM {table} LIMIT {limit}) AS sub_{table}
#         NATURAL JOIN (SELECT * FROM {dates_table} LIMIT {limit}) AS sub_{dates_table}
#         ORDER BY {order_column};
#     """
# }

# Constants representing table and column names
sales_tbls = [
    # "catalog_sales",
    "catalog_sales_ubmark_1000", 
    "catalog_sales_ubmark_10000",
    "catalog_sales_ubmark_100000",
]
items_tbl = "item"
dates_tbl = "date_dim"
order_column = "cs_wholesale_cost"
group_column = "cs_bill_customer_sk"
sales_col = "cs_item_sk"
join_col = "i_item_sk"
range_col = "d_year"
# range_from = 1999
# range_to = 2003
range_from = 5
range_to = 15

def save_query_to_file(query, filename):
    with open(filename, 'w') as file:
        file.write(query)

for sales_tbl in sales_tbls:
    # Generate and save queries
    for query_name, template in tpc_ds_queries.items():
        query = template.format(table=sales_tbl, column=sales_col, alt_table=items_tbl,
                                # join_column=join_col, alt_join_column=join_col,
                                join_column=sales_col, alt_join_column=join_col,
                                range_column=range_col, value_1=range_from, value_2=range_to,
                                group_column=group_column, dates_table=dates_tbl, order_column=order_column)
        
        filename = f"{query_name.replace(' ', '_').lower()}_{sales_tbl}_query.sql"
        # remove parentheses from filename
        filename = filename.replace('(', '').replace(')', '')
        save_query_to_file(query, filename)
        print(f"Saved query '{query_name}' to file '{filename}'")
