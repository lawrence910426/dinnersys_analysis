import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle


from experiment.sum_trend import *
from experiment.amount_figure import *
from experiment.algorithm_compare import *
from output.category_trend import *
from output.prediction import *

# amount_figure("2018-09-20", "2019-01-20" ,60 ,"data_local.pickle")
algorithm_compare()

'''fetch_data.download("data_local.pickle")
data = fetch_data.load("data_local.pickle", "2018-09-01", "2018-11-29")

analysiser = analysis(data, "exists")'''