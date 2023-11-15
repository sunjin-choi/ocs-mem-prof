import subprocess
import os
# looking at tpcds spec for a good table to run 'primitive ops' on
# want at least




def create_index(name, tbl, col):
    create_index_cmd = f"CREATE INDEX {name} ON {tbl} INCLUDES {col}"
    subprocess.Popen(['/usr/bin/psql', 'tpcds', '-c'] + create_index_cmd.split(" "))

def delete_index(name, tbl, col):
    delete_index_cmd = f"drop INDEX {name} ON {tbl} INCLUDES {col}"
    subprocess.Popen(['/usr/bin/psql', 'tpcds', '-c'] + delete_index_cmd.split(" "))

# Dictionary mapping descriptive strings to SQL queries
# TODO indices might have an optimization where even if it's a reference you can read the actual column value directly out of the index and thus avoid ios int
tpc_ds_queries = {
    "Full Scan": "SELECT * FROM {table} WHERE {column} IS NOT NULL;",
    "Cross Join": "SELECT * FROM {table} A CROSS JOIN {alt_table} B;",
    "Equijoin": "SELECT * FROM {table} JOIN {alt_table} ON {table}.{join_column} = {alt_table}.{alt_join_column};",
    "Range Scan": "SELECT * FROM {table} NATURAL JOIN {dates_table} WHERE {range_column} BETWEEN {value_1} AND {value_2};",
    "DISTINCT": "SELECT DISTINCT {column} FROM {table};",
    "Single-Column Aggregation (GROUP BY)": "SELECT {group_column}, COUNT(*) FROM {table} GROUP BY {group_column};",
    "Sort (ORDER BY)": "SELECT * FROM {table} NATURAL JOIN {dates_table} ORDER BY {order_column};",
}

def run_query(query, prefix=""):
    assert prefix == "", "unimplemented lol"
    # TODO should just use path lookup not perl command
    # pager=off disables the 'less' output format (else it hangs forever)
    query_command = ['./bin64/drrun', '-t', 'drcachesim', '-simulator_type', 'elam', '--', 'perl', '/usr/bin/psql', 'tpcds', '-P', "pager=off", '-c', f"'{query}'"]
    query_command = ['perl', '/usr/bin/psql', 'tpcds', '-P', "pager=off", '-c', f"{query}"]
    print(" ".join(query_command))
    proc = subprocess.Popen(query_command)# , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    #print(output)

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

# TODO set up indices and do indices 

# FIX?: equijoin catalog_sales.cs_item_sk
# FIX?: range scan date_dim.d_year
# FIX?: groupby two different columns while aggregate on one column is not a standard sql?

for template in tpc_ds_queries.values():
    os.chdir(os.path.join(os.getenv("DYNAMORIO_HOME"), "build"))
    query = template.format(table=sales_tbl, column=sales_col, alt_table=items_tbl,
                   # join_column=join_col, alt_join_column=join_col,
                   join_column=sales_col, alt_join_column=join_col,
                   range_column=range_col, value_1=range_from, value_2=range_to,
                   group_column=group_column, dates_table=dates_tbl, order_column=order_column)
    run_query(query=query)
