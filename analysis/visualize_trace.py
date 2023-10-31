#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

assert len(sys.argv) > 1, "provide a trace csv file as argument!"

skip_rows = 0
with open(sys.argv[1], 'r') as f:
    for line in f:
        if "---- <application exited with code 0> ----" in line:
            break
        skip_rows += 1

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

# Load the data from the CSV file, skipping the found number of rows
data = pd.read_csv(sys.argv[1], skiprows=range(0, skip_rows + 1), sep=',')

# Group by 1000
data = apply_window_sum(data, 1000)


# Extract the 'x', 'y', and 'z' columns from the DataFrame
x = data['timestamp']
y_hex = data['address']
y = y_hex.apply(lambda x: int(str(x), 16))
z = data['count']


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


# Annotate data points with hexadecimal addresses

# need to do some quantization here lol this generates a billion glyphs
#for i, txt in enumerate(y_hex):
    #ax.text(x[i], y[i], z[i], txt, fontsize=8)

# Display the plot
# plt.show()
plt.savefig(f"{sys.argv[1]}.png")
