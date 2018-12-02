import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle

from internet_data.fetch_data import *

from output.sum_trend import *
from output.category_trend import *

import random

from analysis.micro.micro import *


# fetch_data.download("data_local.pickle")
data = fetch_data.load("data_local.pickle", "2018-09-17", "2018-12-31")
# category_trend(data)


def callback(uid):
    result = mic.get(uid)
    print(result["user id"],
          result["potentials"],
          result["decision"])


mic = micro(data)
mic.train("21005", callback)
mic.train("10123", callback)
mic.train("10119", callback)
mic.train("11707", callback)


# param = np.array([[i] for i in range(50)] ,dtype=np.float)
# value = np.array([[1 if i > 10 else 0 for i in range(50)]] ,dtype=np.float).reshape(50 ,1)
# lo = logistic(param ,value)
# lo.train(step=0.0001 ,cycles=10000 ,output=True)


# for i in range(200):
#     print(param[i] ,value[i] ,lo.query(param[i] ,eplison=0))

# plt.plot([param[i ,0] for i in range(50)] ,[lo.query(param[i]) for i in range(50)])
# plt.plot([param[i ,0] for i in range(50)] ,[value[i ,0]  for i in range(50)])
# plt.show()
