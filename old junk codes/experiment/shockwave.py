from analysis.micro.decision import *
from analysis.micro.booster import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle
import math
import random


def algorithm_compare():
    param = [
        [random.randint(-1, 1) for _ in range(10)] for __ in range(10)
    ]
    value = [random.randint(0, 1) for _ in range(10)]
    print(param)
    print(value)

    data = dict()
    ############################################################################################
    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=20, limit=5, function="train_ternary")
    data["A"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=200, function="train_adagrad")
    data["B"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, beta=0.1, cycles=200, function="train_momentum")
    data["C"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=200, function="train_raw")
    data["D"] = lo.log
    print(lo.cost())
    ############################################################################################

    # plt.xticks(np.arange(0, 3000, 100))
    plt.xlabel('Partial differential executed times', fontsize=15)
    plt.ylabel('Cost function value', fontsize=15)

    plt.plot(data["A"]["gradient"], data["A"]["cost"], label="Ternary precision:5 alpha:8")
    plt.plot(data["B"]["gradient"], data["B"]["cost"], label="Adagrad alpha:8")
    plt.plot(data["C"]["gradient"], data["C"]["cost"], label="Momentum alpha:8 beta:0.9")
    plt.plot(data["D"]["gradient"], data["D"]["cost"], label="Raw alpha:8")
    # plt.plot(data["E"]["gradient"], data["E"]["cost"], label="E")
    # plt.plot(data["F"]["gradient"], data["F"]["cost"], label="F")

    plt.legend(prop={'size': 20})
    plt.show()
