import numpy as np
import math as math
import os
import pandas as pd


class logistic:
    def __init__(self, param, value):  # (0) is the dimension for data rows.
        self.param = self.psuedo_weight(param)
        self.value = value
        self.u_sigmoid = np.frompyfunc(self.sigmoid, 1, 1)
        self.fprime = lambda x, y, w: x.T.dot(
            y.T - self.u_sigmoid(x.dot(w)).T).T  # fprime = d/dw cost
        self.deviation = lambda x: sum([i ** 2 for i in x])
        self.trained = False
        self.log = {"cost": [], "deviation": [], "gradient": []}

    def psuedo_weight(self, item):
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
        self.beta = 0.1 \
            if kwargs.setdefault("beta") is None else kwargs["beta"]
        self.limit = 20 \
            if kwargs.setdefault("limit") is None else kwargs["limit"]
        precision = None \
            if kwargs.setdefault("precision") is None else kwargs["precision"]
        cycles = None \
            if kwargs.setdefault("cycles") is None else kwargs["cycles"]
        output = True \
            if kwargs.setdefault("output") is None else kwargs["output"]

        prev = this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0

        while True:
            if output:
                self.weight = this
                self.log["cost"].append(self.cost())
                self.log["deviation"].append(self.deviation(self.fprime(self.param ,self.value ,this)))
                self.log["gradient"].append(3 * count * self.limit)
            
            prev = this
            this = self.udpate(prev)
            count += 1

            if ((not precision is None) and precision >= logistic.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break

        self.weight = this
        self.trained = True

    def udpate(self, prev):
        # This algorithm is a ternary search. Requires O(log N) time to run
        # I spent a lot of time on it, fuck you.
        # ---------------------------------------------------- #
        origin = self.fprime(self.param, self.value, prev)
        l = 0
        r = self.alpha
        best = r
        count = 0
        while count <= self.limit:
            lmid = (l * 2 + r) / 3
            rmid = (l + r * 2) / 3
            lmid_value = self.fprime(
                self.param, self.value, prev + origin * lmid)
            rmid_value = self.fprime(
                self.param, self.value, prev + origin * rmid)
            if self.deviation(lmid_value) < self.deviation(rmid_value):
                r = rmid
                best = lmid
            if self.deviation(lmid_value) > self.deviation(rmid_value):
                l = lmid
                best = rmid
            if self.deviation(lmid_value) == self.deviation(rmid_value):
                # This is the limitation of the data type, so we break out.
                break
            # print(l, r, lmid ,rmid)
            # print(lmid_value ,rmid_value ,self.deviation(lmid_value), self.deviation(rmid_value))
            count += 1
        return prev + origin * best

        # This shit is working ,please don't modify this.
        # This algorithm runs in a O(N) complexity
        # self.alpha should be an list which size is N and contains all the possible step.
        # ---------------------------------------------------------- #
        # origin = self.fprime(self.param, self.value, prev)
        # best = 0
        # best_v = self.deviation(self.fprime(
        #     self.param, self.value, prev + origin * self.alpha[0]))
        # for i in range(len(self.alpha)):
        #     value = self.deviation(self.fprime(
        #         self.param, self.value, prev + origin * self.alpha[i]))
        #     print(i, self.fprime(self.param, self.value,
        #                          prev + origin * self.alpha[i]), value)
        #     if best_v > value:
        #         best = i
        #         best_v = value
        # print(best, self.alpha[best])
        # return prev + origin * self.alpha[best]

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

    @staticmethod
    def umax(x):    # recursively get the maximum of a ndarray
        if isinstance(x, np.float64) or isinstance(x, float):
            return abs(x)
        maxi = logistic.umax(x[0])
        for i in range(x.shape[0]):
            maxi = logistic.umax(x[i])
        return maxi
