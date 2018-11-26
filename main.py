import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pickle

from internet_data.fetch_data import *
from analysis.analysis import *
from output.trend import *


fetch_data.download("data_local.pickle")

data = fetch_data.load("data_local.pickle" ,"2018-01-01" ,"2018-12-31")

analysiser = analysis(data)

trend(analysiser)
