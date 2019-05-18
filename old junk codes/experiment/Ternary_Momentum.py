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
    lo.train(alpha=16, beta=0.9, limit=50, cycles=50, function="train_ternary_momentum")
    data["A"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=16, beta=0.9, limit=20, cycles=50, function="train_ternary_momentum")
    data["B"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=16, beta=0.1, limit=50, cycles=50, function="train_ternary_momentum")
    data["C"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=16, beta=0.1, limit=20, cycles=50, function="train_ternary_momentum")
    data["D"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, beta=0.9, limit=50, cycles=50, function="train_ternary_momentum")
    data["E"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, beta=0.9, limit=20, cycles=50, function="train_ternary_momentum")
    data["F"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, beta=0.1, limit=50, cycles=50, function="train_ternary_momentum")
    data["G"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=8, beta=0.1, limit=20, cycles=50, function="train_ternary_momentum")
    data["H"] = lo.log
    print(lo.cost())

    lo = logistic(np.array(param, dtype=np.float64),
                  np.array(value, dtype=np.float64))
    lo.train(alpha=0.1, beta=0.1, limit=20, cycles=50, function="train_ternary_momentum")
    data["I"] = lo.log
    print(lo.cost())
    ############################################################################################

    # plt.xticks(np.arange(0, 3000, 100))
    plt.xlabel('Partial differential executed times', fontsize=15)
    plt.ylabel('Cost function value', fontsize=15)

    # plt.plot(data["A"]["gradient"], data["A"]["cost"], label="A") #, marker='x')
    plt.plot(data["B"]["gradient"], data["B"]["cost"], label="B", marker='x')
    # plt.plot(data["C"]["gradient"], data["C"]["cost"], label="C") #, marker='x')
    plt.plot(data["D"]["gradient"], data["D"]["cost"], label="D", marker='x')
    # plt.plot(data["E"]["gradient"], data["E"]["cost"], label="E") #, marker='o')
    plt.plot(data["F"]["gradient"], data["F"]["cost"], label="F", marker='o')
    # plt.plot(data["G"]["gradient"], data["G"]["cost"], label="G") #, marker='o')
    plt.plot(data["H"]["gradient"], data["H"]["cost"], label="H", marker='o')
    # plt.plot(data["I"]["gradient"], data["I"]["cost"], label="I")

    plt.legend(prop={'size': 20})
    plt.show()
