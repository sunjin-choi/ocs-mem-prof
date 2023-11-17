
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS
import sys


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

def draw_scatter_plot(data, length, start_idx):
    data_plot = trim_data(data, length, start_idx)
    x, y, z = extract_cols(data_plot)
    
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a wireframe 3D plot
    ax.scatter(x, y, z, c='b', marker='o')
    
    # Set labels for the axes
    ax.set_xlabel('timestamp')
    ax.set_ylabel('address')
    ax.set_zlabel('frequency')
    ax.set_title('Stores and Loads')