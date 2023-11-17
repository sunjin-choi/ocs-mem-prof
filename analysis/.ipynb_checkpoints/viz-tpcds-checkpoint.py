import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d  # noqa: F401

from sklearn.cluster import OPTICS
from sklearn import datasets
from sklearn.cluster import KMeans

from viztools import draw_scatter_plot, data_loader

trace_dir = "/tmp/tpcds-trace"

machine_name = "n1-standard-8"
query_data = "scale_1_rngseed_0"
query_limit = False
query_name = "3"

data = data_loader(trace_dir, query_name, query_data, query_limit, machine_name)
fig = draw_scatter_plot(data, False, -1, -1, True, 10)

fig.savefig(f"plots/tpcds_{query_name}/{machine_name}_{query_data}.png")
