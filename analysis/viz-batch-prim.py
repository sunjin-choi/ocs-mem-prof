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

machine_name = lambda patch: "n2-standard-8" if patch is False else "test"
query_data = "scale_1_rngseed_0"
query_limit = 100

query_names = ["distinct", "cross_join", "equijoin" ,"fullscan", "range_scan", "single-column_aggregation_group_by", "sort_order_by"]

# make plots directory
if not os.path.exists("plots"):
    os.makedirs("plots")

for query_name in query_names:
    patch = True if query_name in ["cross_join", "sort_order_by"] else False
    data = data_loader(trace_dir, query_name, query_data, query_limit, machine_name(patch))

    # make directory with query name if it doesn't exist
    if not os.path.exists("plots/" + query_name):
        os.makedirs("plots/" + query_name)
        
    print(f"generating figures for {query_name}")

    fig_trimmed = draw_scatter_plot(data, True, int(5e6), int(1e6), True, 10)
    fig_trimmed.savefig(f"plots/{query_name}/{machine_name(patch)}_{query_data}_{query_limit}_trimmed.png")

    fig_full = draw_scatter_plot(data, False, -1, -1, True, 10)
    fig_full.savefig(f"plots/{query_name}/{machine_name(patch)}_{query_data}_{query_limit}.png")
