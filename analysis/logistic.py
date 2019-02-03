import numpy as np
import math as math
import os


class logistic:
    def __init__(self, param, value):  # (0) is the dimension for data rows.
        self.param = self.psuedo_weight(param)
        self.value = value
        self.u_sigmoid = np.frompyfunc(self.sigmoid, 1, 1)
        self.fprime = lambda x, y, w: x.T.dot(
            y.T - self.u_sigmoid(x.dot(w)).T).T  # fprime = d/dw cost
        self.trained = False

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
        self.step = 1 if kwargs.setdefault("step") is None else kwargs["step"]
        self.delta = 0.5 if kwargs.setdefault("delta") is None else kwargs["delta"]
        precision = None if kwargs.setdefault(
            "precision") is None else kwargs["precision"]
        cycles = None if kwargs.setdefault(
            "cycles") is None else kwargs["cycles"]
        output = True if kwargs.setdefault(
            "output") is None else kwargs["output"]

        prev = this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0

        while True:
            prev = this
            this = self.udpate(prev)
            count += 1

            if output:
                print("normal iterate: ", prev, this, logistic.umax(
                    prev - this), self.fprime(self.param, self.value, prev), count)
                # os.system("pause")

            if ((not precision is None) and precision >= logistic.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break

        self.weight = this
        self.trained = True

    def udpate(self, prev):
        origin = self.fprime(self.param, self.value, prev)
        tmp = prev + self.step * origin

        def greater(a, b):
            for i in range(a.shape[0]):
                if abs(a[i]) < abs(b[i]) - self.delta:
                    return False
            return True

        while not greater(origin, self.fprime(self.param, self.value, tmp)):
            self.step *= self.delta
            tmp = prev + self.step * origin
            print("udpate alpha: ", self.step,
                  prev, origin,
                  tmp, self.fprime(self.param, self.value, tmp))
            os.system("pause")
        return tmp

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
            summa += self.value[i] * math.log(tmp) + (1 - self.value[i]) * \
                math.log(1 - tmp)
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
