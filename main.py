import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle

from internet_data.fetch_data import *

from experiment.sum_trend import *
from experiment.amount_figure import *
from experiment.algorithm_compare import *
from output.category_trend import *
from output.prediction import *

from analysis.logistic.logistic import *

amount_figure("2018-09-17", "2019-01-17" ,30 ,"data_local.pickle")
# algorithm_compare()

# fetch_data.download("data_local.pickle")
# data = fetch_data.load("data_local.pickle", "2018-09-01", "2018-11-29")

# analysiser = analysis(data, "exists")

# def callback(uid):
#     print("done training")

# booster = booster()
# tmp = {
#     "2018-09-01" :True,
#     "2018-09-02" :None,
#     "2018-09-03" :None,
#     "2018-09-04" :True,
#     "2018-09-05" :None,
#     "2018-09-06" :None,
#     "2018-09-07" :True,
#     "2018-09-08" :None,
#     "2018-09-09" :None
# }
# decision = decision(tmp ,3 ,1)
# decision.train(booster ,callback)

