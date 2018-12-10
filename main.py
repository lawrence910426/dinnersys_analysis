import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle

from internet_data.fetch_data import *

from output.sum_trend import *
from output.category_trend import *
from output.amount_figure import *
from output.prediction import *

# fetch_data.download("data_local.pickle")
data = fetch_data.load("data_local.pickle", "2018-09-17", "2018-12-31")
prediction(data)


