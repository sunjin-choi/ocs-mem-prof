import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d  # noqa: F401

from sklearn.cluster import OPTICS
from sklearn import datasets
from sklearn.cluster import KMeans

from viztools import draw_scatter_plot, data_loader

trace_dir = "/tmp/tpcds-trace"

machine_name = "n2-standard-8"
query_data = "scale_1_rngseed_0"
query_limit = 100

query_names = ["distinct", "cross_join", "equijoin" ,"fullscan", "range_scan", "single-column_aggregation_group_by", "sort_order_by"]

# make plots directory
if not os.path.exists("plots"):
    os.makedirs("plots")

for query_name in query_names:
    data = data_loader(trace_dir, query_name, query_data, query_limit, machine_name)
    fig = draw_scatter_plot(data, True, int(1e6), 0, True, 10)

    # make directory with query name if it doesn't exist
    if not os.path.exists("plots/" + query_name):
        os.makedirs("plots/" + query_name)

    fig.savefig(f"plots/{query_name}/{machine_name}_{query_data}_{query_limit}.png")
