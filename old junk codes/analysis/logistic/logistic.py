import numpy as np
import math as math
import os
import pandas as pd
from analysis.logistic.train import train


class logistic(train):
    def __init__(self, param, value):  # (0) is the dimension for data rows.
        self.param = self.psuedo_weight(param)
        self.value = value
        self.u_sigmoid = np.frompyfunc(self.sigmoid, 1, 1)
        self.deviation = lambda x: sum([i ** 2 for i in x])
        self.trained = False
        self.log = {"cost": [], "deviation": [], "gradient": []}

    def fprime(self ,x ,y ,w): # fprime = d/dw cost
        row_vector_w = w.reshape((self.param.shape[1], 1))
        dotted = x.dot(row_vector_w)
        sigmoided = self.u_sigmoid(dotted)
        row_vector_y = y.reshape((self.param.shape[0], 1))
        grad = x.T.dot(row_vector_y - sigmoided).T[0]
        return np.clip(grad ,-5 ,5)

    def psuedo_weight(self, item):
        return item
        if len(item.shape) == 2:    # the exam set
            tmp = np.zeros((item.shape[0], item.shape[1] + 1))
            tmp[:, :-1] = item
            tmp[:, -1] = [1 for i in range(item.shape[0])]
        if len(item.shape) == 1:    # the answer set
            tmp = np.zeros((item.shape[0] + 1))
            tmp[:-1] = item
            tmp[-1] = 1
        return tmp

    def train(self, **kwargs):
        self.alpha = 2 \
            if kwargs.setdefault("alpha") is None else kwargs["alpha"]
        self.beta = 0.9 \
            if kwargs.setdefault("beta") is None else kwargs["beta"]
        self.limit = 25 \
            if kwargs.setdefault("limit") is None else kwargs["limit"]
        precision = None \
            if kwargs.setdefault("precision") is None else kwargs["precision"]
        cycles = None \
            if kwargs.setdefault("cycles") is None else kwargs["cycles"]
        output = True \
            if kwargs.setdefault("output") is None else kwargs["output"]
        function = "train_raw" \
            if kwargs.setdefault("function") is None else kwargs["function"]
        
        getattr(self, function)(precision ,cycles ,output)
        self.trained = True

    def query(self, value ,psuedo=True):
        if psuedo:
            value = self.psuedo_weight(value)
        tmp = value.dot(self.weight)
        return self.sigmoid(tmp)

    def cost(self):
        summa = 0
        for i in range(len(self.param)):
            tmp = self.query(self.param[i] ,False)
            if self.value[i] == 0:
                summa += 0 if tmp == 1 else math.log(1 - tmp)
            if self.value[i] == 1:
                summa += 0 if tmp == 0 else math.log(tmp)
        return summa

    @staticmethod
    def sigmoid(x):
        if x <= -700:
            return 1
        return 1 / (1 + math.exp(-x))
