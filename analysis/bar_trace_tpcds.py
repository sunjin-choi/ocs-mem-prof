import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import glob
import os

# Specify the directory containing the CSV files
directory = '/tmp/db-ubmark-trace/samples_1000000'

# Read all CSV files in the directory
all_files = glob.glob(os.path.join(directory, "*.csv"))

# Concatenate all CSV files into a single DataFrame
all_data = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

import pdb; pdb.set_trace()

#
# # Get unique values for CacheName and TraceFile
# unique_cache_names = all_data['CacheName'].unique()
# unique_trace_files = all_data['TraceFile'].unique()
#
# # Initialize data for plotting
# plot_data = pd.DataFrame()
#
# # Fill in the data for plotting
# for trace_file in unique_trace_files:
#     for cache_name in unique_cache_names:
#         # Filter data for the current combination of TraceFile and CacheName
#         subset = all_data[(all_data['TraceFile'] == trace_file) & (all_data['CacheName'] == cache_name)]
#
#         # Summarize data and add to plot_data
#         plot_data = plot_data.append({
#             'TraceFile': trace_file,
#             'CacheName': cache_name,
#             'NFMMisses': subset['NFMMisses'].sum(),
#             'BackingStoreMisses': subset['BackingStoreMisses'].sum()
#         }, ignore_index=True)
#
# # Melt the data for seaborn plotting
# melted_data = plot_data.melt(id_vars=['TraceFile', 'CacheName'], var_name='Metric', value_name='Misses')
#
# # Plotting
# plt.figure(figsize=(12, 6))
# sns.barplot(x='TraceFile', y='Misses', hue='Metric', data=melted_data)
#
# # Customize plot (you can adjust these parameters for your paper quality)
# plt.xticks(rotation=45)
# plt.xlabel('Trace File')
# plt.ylabel('Number of Misses')
# plt.title('Number of Misses by Cache Name and Trace File')
# plt.legend(title='Miss Type', loc='upper right')
# plt.tight_layout()
#
# # Show/save the plot
# plt.show()
# plt.savefig('bar_chart.png', dpi=300) # Uncomment to save the figure

