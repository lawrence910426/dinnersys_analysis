import numpy as np
import math as math
import os


class logistic:
    def __init__(self, param, value):  # [0] is the dimension for data rows.
        self.param = self.psuedo_weight(param)
        self.value = value
        self.u_sigmoid = np.frompyfunc(self.sigmoid, 1, 1)
        self.trained = False

    def psuedo_weight(self, item):
        if len(item.shape) == 2:
            tmp = np.zeros((item.shape[0], item.shape[1] + 1))
            tmp[:, :-1] = item
            tmp[:, -1] = [1 for i in range(item.shape[0])]
        if len(item.shape) == 1:
            tmp = np.zeros((item.shape[0] + 1))
            tmp[:-1] = item
            tmp[-1] = 1
        return tmp

    def train(self, **kwargs):
        step = 0.0001 if kwargs.setdefault("step") is None else kwargs["step"]
        precision = None if kwargs.setdefault(
            "precision") is None else kwargs["precision"]
        cycles = None if kwargs.setdefault(
            "cycles") is None else kwargs["cycles"]
        output = True if kwargs.setdefault(
            "output") is None else kwargs["output"]

        prev = np.array(
            [-1 for i in range(len(self.param[0]))], dtype=np.float)
        this = prev + \
            np.array([0.01 for i in range(len(self.param[0]))], dtype=np.float)

        count = 0
        while True if precision is None else logistic.umax(prev - this) > precision:
            tmp = this
            delta = self.fprime(prev, step, self.param, self.value)
            this = tmp + delta
            prev = tmp
            count += 1
            if count >= cycles and (not cycles is None):
                break
            if output:
                print(prev, delta, logistic.umax(prev - this), count)

        self.weight = this
        self.trained = True

    def fprime(self, prev, alpha, x, y):
        tmp = y.T - self.u_sigmoid(x.dot(prev))
        return alpha * x.T.dot(tmp.T).T[0]

    def query(self, value, **kwargs):
        if self.trained:
            tmp = self.weight.dot(self.psuedo_weight(value))
            return self.sigmoid(tmp)
        else:
            return 0

    def cost(self):
        summa = 0
        for i in range(len(self.param)):
            tmp = logistic.sigmoid(self.weight.dot(self.param[i]))
            summa += self.value[i] * math.log(tmp) + (1 - self.value[i]) * math.log(1 - tmp)
        return summa

    @staticmethod
    def sigmoid(x):
        if x <= -700:
            return 1
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def umax(x):
        if isinstance(x, np.float64) or isinstance(x, float):
            return abs(x)
        maxi = logistic.umax(x[0])
        for i in range(x.shape[0]):
            maxi = logistic.umax(x[i])
        return maxi
