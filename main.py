import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle

from internet_data.fetch_data import *

from experiment.sum_trend import *
from output.category_trend import *
from output.amount_figure import *
from output.prediction import *

from analysis.logistic.logistic import *
# from analysis.micro.decision import *
# from analysis.micro.booster import *

# param = [
#     [-1, 1, -1, -1, -1],
#     [-1, 1, -1, -1, -1],
#     [-1, 1, -1, 1, -1],
#     [1, 1, -1, -1, -1],
#     [1, -1, 1, 1, 1],
#     [1, 1, 1, -1, 1],
# ]
# value = [0, 0, 1, 1, 1, 0]

# data = dict()

# ############################################################################################
# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=0.001 ,cycles=550 ,function="train_raw")
# data["R_C"] = lo.cost()
# data["R"] = lo.log

# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=0.001 ,beta=0.5 ,cycles=550 ,function="train_momentum")
# data["M_C"] = lo.cost()
# data["M"] = lo.log

# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=2 ,cycles=600 ,function="train_raw")
# data["OR_C"] = lo.cost()
# data["OR"] = lo.log

# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=2 ,beta=0.5 ,cycles=500 ,function="train_momentum")
# data["OM_C"] = lo.cost()
# data["OM"] = lo.log

# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=8 ,limit=20 ,cycles=10 ,function="train_ternary")
# data["T_C"] = lo.cost()
# data["T"] = lo.log

# lo = logistic(np.array(param, dtype=np.float64),
#               np.array(value, dtype=np.float64))
# lo.train(alpha=8 ,beta=0.1 ,limit=20 ,cycles=10 ,function="train_ternary_momentum")
# data["TM_C"] = lo.cost()
# data["TM"] = lo.log
# ############################################################################################

# fig, ax = plt.subplots()

# plt.xticks(np.arange(0, 3000, 100))
# plt.xlabel('Partial differential executed times' ,fontsize=15)
# plt.ylabel('Cost function value' ,fontsize=15)

# plt.plot(data["R"]["gradient"], data["R"]["cost"] ,label=u"Raw Gradient")
# plt.plot(data["M"]["gradient"], data["M"]["cost"] ,label=u"Momentum")
# # plt.plot(data["R"]["gradient"], data["OR"]["cost"] ,label=u"Raw Gradient Oversize")
# # plt.plot(data["M"]["gradient"], data["OM"]["cost"] ,label=u"Momentum Oversize")
# plt.plot(data["T"]["gradient"], data["T"]["cost"] ,label=u"Ternary")
# plt.plot(data["TM"]["gradient"], data["TM"]["cost"] ,label=u"Ternary + Momentum")

# plt.legend(prop={'size': 20})
# plt.show()


# fetch_data.download("data_local.pickle")
# data = fetch_data.load("data_local.pickle", "2018-09-01", "2018-11-29")
amount_figure("2018-09-17", "2019-01-31" ,60)
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

