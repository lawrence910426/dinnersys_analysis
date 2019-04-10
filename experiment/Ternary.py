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
    lo.train(alpha=16, cycles=50, limit=50 ,function="train_ternary")
    data["A"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=16, cycles=50, limit=20 ,function="train_ternary")
    data["B"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=50, limit=50 ,function="train_ternary")
    data["C"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=50, limit=20 ,function="train_ternary")
    data["D"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, cycles=50, limit=5 ,function="train_ternary")
    data["E"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=0.1, cycles=50, limit=20 ,function="train_ternary")
    data["F"] = lo.log
    print(lo.cost())
    ############################################################################################

    # plt.xticks(np.arange(0, 3000, 100))
    plt.xlabel('Partial differential executed times', fontsize=15)
    plt.ylabel('Cost function value', fontsize=15)

    plt.plot(data["A"]["gradient"], data["A"]["cost"], label="A" ,marker='x')
    plt.plot(data["B"]["gradient"], data["B"]["cost"], label="B" ,marker='x')
    plt.plot(data["C"]["gradient"], data["C"]["cost"], label="C")
    plt.plot(data["D"]["gradient"], data["D"]["cost"], label="D")
    # plt.plot(data["E"]["gradient"], data["E"]["cost"], label="E")
    # plt.plot(data["F"]["gradient"], data["F"]["cost"], label="F")

    plt.legend(prop={'size': 20})
    plt.show()