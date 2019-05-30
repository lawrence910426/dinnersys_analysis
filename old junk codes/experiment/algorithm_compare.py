from analysis.micro.decision import *
from analysis.micro.booster import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle


def algorithm_compare():
    param = [
        [-1, 1, -1, -1, -1],
        [-1, 1, -1, -1, -1],
        [-1, 1, -1, 1, -1],
        [1, 1, -1, -1, -1],
        [1, -1, 1, 1, 1],
        [1, 1, 1, -1, 1],
        [-1, -1, 1, -1, -1],
        [1, -1, 1, -1, 1],
        [-1, -1, 1, -1, 1],
        [1, 1, 1, -1, -1],
    ]
    value = [0, 0, 1, 1, 1, 0 ,1 ,1, 0 ,1]

    data = dict()

    ############################################################################################
    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=0.1, cycles=200, function="train_adagrad")
    data["A"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=4, limit=10 ,cycles=20, function="train_ternary")
    data["B"] = lo.log
    print(lo.cost())
    ############################################################################################

    # plt.xticks(np.arange(0, 3000, 100))
    plt.xlabel('Partial differential executed times', fontsize=15)
    plt.ylabel('Cost function value', fontsize=15)

    plt.plot(data["A"]["gradient"], data["A"]["cost"], label="Adagrad alpha:0.1")
    plt.plot(data["B"]["gradient"], data["B"]["cost"], label="Ternary alpha:4 precision:5")
    plt.plot(data["C"]["gradient"], data["C"]["cost"], label="Momentum alpha:0.001 beta:0.9")

    plt.legend(prop={'size': 20})
    plt.show()
