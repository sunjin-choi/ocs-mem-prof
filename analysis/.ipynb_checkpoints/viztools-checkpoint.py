from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS
import sys
import mpl_toolkits.mplot3d  # noqa: F401

from sklearn import datasets
from sklearn.cluster import KMeans

def apply_window_sum(data, group_size):
    """
    Apply a summing window of given size to the data for coarser granular analysis.
    The function groups data into batches of 'group_size' and then sums them.
    """
    # Create a 'group' column that identifies which group each row belongs to
    data['group'] = data.index // group_size

    # Group by 'group' and sum up the other columns
    windowed_data = data.groupby('group').agg({
        'timestamp': 'mean',  # or 'first', depending on what you want
        'address': 'first',  # keeping the first address for each group
        'count': 'sum'
    }).reset_index(drop=True)

    return windowed_data

def select_top_n(data, n):
    """
    Select the top n most frequently accessed addresses.
    """
    return data.groupby('address').sum().sort_values(by='count', ascending=False).head(n)

def trim_data(data, window_size, start_idx):
    """
    Trim the data to the given window size.
    """

    # Trim the data to the given window size
    data = data.iloc[start_idx:start_idx+window_size]

    # Reset the index
    data = data.reset_index(drop=True)
    
    return data

def extract_cols(data):
    x = data['timestamp']
    y = (data['address']).apply(lambda x: int(str(x), 16))
    z = data['count']
    return x, y, z

def data_loader(trace_dir, query_name, query_data, query_limit, machine_name):
    def file_path(query_name, query_data=query_data, query_limit=query_limit, machine_name=machine_name):
        if query_limit is False:
            return Path(trace_dir) / f"query_{query_name}_{query_data}_{machine_name}.csv"
        else: 
            return Path(trace_dir) / f"query_{query_name}_{query_data}_{machine_name}-limit-{query_limit}.csv"

    skip_rows = 0
    with open(file_path(query_name), 'r') as f:
        for line in f:
            if "---- <application exited with code 0> ----" in line:
                break
            skip_rows += 1
    
    # Load the data from the CSV file, skipping the found number of rows
    data = pd.read_csv(file_path(query_name), skiprows=range(0, skip_rows + 1), sep=',')
    return data[["timestamp", "address", "count"]]

def draw_scatter_plot(data, trim, length, start_idx, kmeans, n_clusters):
    if trim:
        data_plot = trim_data(data, length, start_idx)
        print(f"trace plot of execution time {100*start_idx/len(data):.3f}% to {100*(start_idx+length)/len(data):.3f}%")
    else:
        data_plot = data
        print(f"full trace plot")
    
    if kmeans:
        est = KMeans(n_clusters=n_clusters, n_init="auto")
        est.fit(data_plot)
        labels = est.labels_   

    # Create a 3D plot
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(1, 1, 1, projection="3d", elev=48, azim=134)
    
    # Create a wireframe 3D plot
    x, y, z = extract_cols(data_plot)
    ax.scatter(x, y, z, c=labels.astype(float) if kmeans else 'b', edgecolor="k")
    
    # Set labels for the axes
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([]) 
    ax.set_xlabel('timestamp')
    ax.set_ylabel('address')
    ax.set_zlabel('frequency')
    ax.set_title('Stores and Loads')

    return fig

