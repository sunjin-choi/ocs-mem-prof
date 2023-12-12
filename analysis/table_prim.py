import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import glob
import os

# Specify the directory containing the CSV files
directory = './data_db_ubmark/samples_1000000'

# Read all CSV files in the directory
all_files = glob.glob(os.path.join(directory, "*.csv"))

# Concatenate all CSV files into a single DataFrame
all_data = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)


# Get unique values for CacheName and TraceFile
unique_cache_names = all_data['Cache Name'].unique()
unique_trace_files = all_data[' Trace File'].unique()

# Initialize data for plotting
plot_data = pd.DataFrame()

def parse_and_format_filename(filename):
    # Extract the part of the filename between 'query_' and '_scale'
    start = filename.find('query_') + 6  # 6 is the length of 'query_'
    end = filename.find('_scale')
    segment = filename[start:end]

    # Replace underscores and hyphens with spaces
    formatted_segment = segment.replace('_', ' ').replace('-', ' ')

    # Capitalize each word
    formatted_segment = formatted_segment.title()

    return formatted_segment



# Fill in the data for plotting
for trace_file in unique_trace_files:
    for cache_name in unique_cache_names:
        # Filter data for the current combination of TraceFile and CacheName
        subset = all_data[(all_data[' Trace File'] == trace_file) & (all_data['Cache Name'] == cache_name)]
        subset = subset[(all_data[' Trace File'].str.contains('1000'))]

        # Summarize data and add to plot_data
        plot_data = plot_data.append({
            'TraceFile': parse_and_format_filename(trace_file),
            'CacheName': cache_name,
            'NFMMisses': subset[' NFM Misses'].sum(),
            'BackingStoreMisses': subset[' Backing Store Misses'].sum()
        }, ignore_index=True)

# Melt the data for seaborn plotting
melted_data = plot_data.melt(id_vars=['TraceFile', 'CacheName'], var_name='Metric', value_name='Misses')

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
ax = sns.barplot(x='TraceFile', y='Misses', hue='Metric', data=melted_data)

# Set the font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Customize plot (you can adjust these parameters for your paper quality)
# plt.xticks(rotation=45)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontname='Times New Roman', fontsize=12)
ax.set_xlabel('Trace File', fontsize=12, fontname='Times New Roman')
ax.set_ylabel('Number of Misses', fontsize=12, fontname='Times New Roman')
plt.title('Number of Misses by Cache Name and Trace File', fontsize=20, fontname='Times New Roman')
plt.legend(title='Miss Type', loc='upper right')
plt.tight_layout()

# # plot table
# fig, ax = plt.subplots()
# ax.table(cellText=plot_data.values, colLabels=plot_data.columns, loc='center')
# ax.axis('off')


# Show/save the plot
plt.show()
plt.savefig('bar_chart.png', dpi=300) # Uncomment to save the figure

