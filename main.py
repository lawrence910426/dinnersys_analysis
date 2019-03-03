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

from analysis.logistic import *
# from analysis.micro.decision import *
# from analysis.micro.booster import *

param = [
    [-1, 1, -1, -1, -1],
    [-1, 1, -1, -1, -1],
    [-1, 1, -1, 1, -1],
    [1, 1, -1, -1, -1],
    [1, -1, 1, 1, 1],
    [1, 1, 1, -1, 1],
]
value = [0, 0, 1, 1, 1, 0]
lo = logistic(np.array(param, dtype=np.float64),
              np.array(value, dtype=np.float64))
lo.train(alpha=2 ,limit=10 ,cycles=30)

fig, ax = plt.subplots()

mini = min(lo.log["gradient"])
maxi = max(lo.log["gradient"])
plt.xticks(np.arange(mini, maxi + 1, (maxi - mini) / len(lo.log["gradient"])))

# plt.bar(lo.log["gradient"], lo.log["cost"]         ,label="cost_function")
plt.plot(lo.log["gradient"], lo.log["cost"]         ,label="cost_function")
# plt.bar(lo.log["gradient"], lo.log["deviation"]    ,label="deviation")
plt.plot(lo.log["gradient"], lo.log["deviation"]         ,label="deviation")

plt.legend()
plt.show()

print(lo.query(np.array([0, 1, 0, 0, 0])))

# fetch_data.download("data_local.pickle")
# data = fetch_data.load("data_local.pickle", "2018-09-17", "2018-12-06")
# analysiser = analysis(data, "exists")

# def callback(uid):
#     print(decision.get())
#     print(decision.neuron.loaded)
#     print(decision.neuron.loaded["function"].weight)

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
