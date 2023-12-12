import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import glob
import os

# Specify the directory containing the CSV files
directory = "./data_db_tpcds/samples_1000000"

# Read all CSV files in the directory
all_files = glob.glob(os.path.join(directory, "*.csv"))

# Concatenate all CSV files into a single DataFrame
all_data = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# Get unique values for CacheName and TraceFile
unique_cache_names = all_data["Cache Name"].unique()
unique_trace_files = all_data[" Trace File"].unique()

# Initialize data for plotting
plot_data = pd.DataFrame()


def parse_and_format_filename(filename):
    # Extract the part of the filename between 'query_' and '_scale'
    start = filename.find("query_") + 6  # 6 is the length of 'query_'
    end = filename.find("_scale")
    segment = filename[start:end]

    # Replace underscores and hyphens with spaces
    formatted_segment = segment.replace("_", " ").replace("-", " ")

    return formatted_segment

# Fill in the data for plotting
for trace_file in unique_trace_files:
    if int(parse_and_format_filename(trace_file)) < 35: 
        for cache_name in unique_cache_names:
            # Filter data for the current combination of TraceFile and CacheName and TraceFile contains '1000'

            subset = all_data[
                (all_data[" Trace File"] == trace_file)
                & (all_data["Cache Name"] == cache_name)
            ]
            # subset = all_data[(all_data[' Trace File'] == trace_file) & (all_data['Cache Name'] == cache_name)]
            # subset = subset[(all_data[' Trace File'].str.contains('1000'))]

            # Summarize data and add to plot_data
            plot_data = plot_data.append(
                {
                    "TraceFile": parse_and_format_filename(trace_file),
                    "CacheName": cache_name,
                    "DRAMAccesses": subset[" DRAM Accesses"].sum(),
                    "NFMHits": subset[" NFM hits"].sum(),
                    "NFMMisses": subset[" NFM Misses"].sum(),
                    "BackingStoreHits": subset[" Backing Store hits"].sum(),
                    "BackingStoreMisses": subset[" Backing Store Misses"].sum(),
                },
                ignore_index=True,
            )


# Prepare data for stacked bar chart
grouped_data = plot_data.groupby(["TraceFile", "CacheName"]).sum().reset_index()

# Create a color map for the metrics
# colors = ["skyblue", "orange", "green", "red", "purple"]
# Using 'tab10' colormap
# tab10_colors = plt.cm.tab10.colors  # Get colors from 'tab10' colormap
# colors = [tab10_colors[0], tab10_colors[1], tab10_colors[3], tab10_colors[4], tab10_colors[7]]

# colorsmap = plt.cm.cividis.colors  # Get colors from 'viridis' colormap
# colors = colorsmap[::int(len(colorsmap)/5)][:5]  # Select five distinct colors

# set2_colors = plt.cm.Set2.colors  # Get colors from 'Set2' colormap
# colors = set2_colors[:5]  # Select the first five colors

# colors = ["#1f77b4", "#ff7f0e", "#8c564b", "#d62728", "#9467bd"]
colors = ["#1f77b4", "#ff7f0e", "#8c564b", "#d62728", "#9467bd", "#f0f8ff"]  # Modified hex codes
metric_columns = [
    "DRAMAccesses",
    "NFMHits",
    "NFMMisses",
    "BackingStoreHits",
    "BackingStoreMisses",
]

# Plotting
fig, ax = plt.subplots(figsize=(17, 5))

# Set the font to Times New Roman
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

# Width of a bar and gap between groups
bar_width = 0.1
gap_bar_width = 0.05
gap_group_width = 0.3  # Width of the gap between groups

# TraceFile and CacheName for plotting
trace_files = grouped_data["TraceFile"].unique()
cache_names = grouped_data["CacheName"].unique()

def reorder_cache_names(cache_names):
    # Define the custom order
    order_map = {
        'OCS cache with random conservative replacement for both NFM and backing store': 0,
        'OCS cache with random liberal replacement for both NFM and backing store': 1,
        'OCS cache with clock replacement for both NFM and backing store': 2,
        'Pure Far-Memory Cache with random replacement': 3,
        'Far Memory cache with clock replacement for both NFM and backing store': 4
    }

    # Sort the array based on the custom order
    sorted_cache_names = sorted(cache_names, key=lambda x: order_map.get(x, 5))

    return np.array(sorted_cache_names)

def filter_cache_names(cache_names):
    # Define the custom order
    order_map = {
        'OCS cache with random conservative replacement for both NFM and backing store': 0,
        'OCS cache with clock replacement for both NFM and backing store': 1,
        'Pure Far-Memory Cache with random replacement': 2,
        'Far Memory cache with clock replacement for both NFM and backing store': 3
    }

    # Sort the array based on the custom order
    filtered_cache_names = [cache_name for cache_name in cache_names if cache_name in order_map.keys()]
    sorted_cache_names = sorted(filtered_cache_names, key=lambda x: order_map.get(x, 5))
    return sorted_cache_names

# cache_names = reorder_cache_names(cache_names)
cache_names = filter_cache_names(cache_names)

def reorder_trace_names(trace_files):
    sorted_trace_files = sorted(trace_files, key=lambda x: int(x))
    return np.array(sorted_trace_files)

trace_files = reorder_trace_names(trace_files)

# Calculate positions for the bars
n_trace_files = len(trace_files)
n_caches = len(cache_names)
group_width = n_caches * (bar_width + gap_bar_width) + gap_group_width
bar_l = [i * group_width for i in range(n_trace_files)]

# Keep track of labels added to avoid duplicates in the legend
added_labels = set()

# Plotting bars
for i, trace_file in enumerate(trace_files):
    for idx, cache_name in enumerate(cache_names):
        subset = grouped_data[
            (grouped_data["CacheName"] == cache_name)
            & (grouped_data["TraceFile"] == trace_file)
        ]
        bottom_pos = 0
        bar_position = bar_l[i] + idx * bar_width + (idx-1) * gap_bar_width
        for metric in metric_columns:
            label = metric if metric not in added_labels else ""
            added_labels.add(metric)
            ax.bar(
                bar_position,
                subset[metric].sum(),
                color=colors[metric_columns.index(metric)],
                width=bar_width,
                label=label,
                bottom=bottom_pos,
                edgecolor="black",
            )
            bottom_pos += subset[metric].sum()


# Customizing the plot

# Adjusted calculations for ax xticks
bar_centers = [bar_l[i] + ((idx-1) * (bar_width + gap_bar_width)) + bar_width for i in range(n_trace_files) for idx in range(n_caches)]
ax.set_xticks(bar_centers)
ax.set_xticklabels([f"{i+1}" for i in range(n_caches)] * n_trace_files, rotation=0, horizontalalignment="center",
                   fontsize=8)

# TraceFile labels (secondary labels below CacheName labels)
# ax.set_xlabel('Cache Name', fontsize=12, fontname='Times New Roman')
ax.tick_params(
    axis="x", which="major", pad=15
)  # Increase space between ticks and labels
ax2 = ax.twiny()  # New axis for TraceFile labels
ax2.set_xlim(ax.get_xlim())

# Adjusted calculations for ax2 xticks
group_centers = [group_width * i + ((n_caches * bar_width + 1 * gap_bar_width) / 2) for i in range(n_trace_files)]
ax2.set_xticks(group_centers)
ax2.set_xticklabels(trace_files, rotation=0, horizontalalignment="center")

ax2.xaxis.set_ticks_position("bottom")  # Position of the second x-axis
ax2.spines["bottom"].set_position(("outward", 40))  # Move the second x-axis lower
# ax2.set_xlabel('Trace File', fontsize=12)

ax.set_ylabel("Memory Access Classification", fontsize=12, fontname="Times New Roman")
plt.title("Simulated Memory Access Breakdown on TPC-DS Query Traces", fontsize=20, fontname="Times New Roman")
# plt.legend(title='Metric Type', loc='upper right')
# ax.legend(loc="lower right", title="Access Type")
ax.legend(loc="lower right", title="Access Type", bbox_to_anchor=(1.0, 0.0), ncol=1, borderaxespad=0.0)

fig.tight_layout()

# Show/save the plot
plt.show()
plt.savefig("stacked_bar_chart.png", dpi=300)
