import numpy as np
import math as math
import os
import pandas as pd


class train:
    def train_raw(self, precision, cycles, output):
        this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0
        while True:
           
            if output:
                self.weight = this
                self.log["cost"].append(self.cost())
                self.log["deviation"].append(self.deviation(
                    self.fprime(self.param, self.value, this)))
                self.log["gradient"].append(count)
            
            slope = self.fprime(self.param, self.value, this)
            this = this + slope * self.alpha

            count += 1
            
            if ((not precision is None) and precision >= train.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break
        self.weight = this

    def train_ternary(self, precision, cycles, output):
        this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0
        while True:
            if output:
                self.weight = this
                self.log["cost"].append(self.cost())
                self.log["deviation"].append(self.deviation(
                    self.fprime(self.param, self.value, this)))
                self.log["gradient"].append(3 * count * self.limit)

            this = this + self.ternary(this)
            count += 1

            if ((not precision is None) and precision >= train.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break
        self.weight = this

    def train_momentum(self, precision, cycles, output):
        prev = this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0
        while True:
            if output:
                self.weight = this
                self.log["cost"].append(self.cost())
                self.log["deviation"].append(self.deviation(
                    self.fprime(self.param, self.value, this)))
                self.log["gradient"].append(count)

            slope = self.fprime(self.param, self.value, this)
            tmp = slope * self.alpha + prev * self.beta
            this = this + tmp
            prev = tmp

            count += 1

            if ((not precision is None) and precision >= train.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break
        self.weight = this

    def train_ternary_momentum(self, precision, cycles, output):
        prev = this = np.zeros((len(self.param[0])), dtype=np.float)
        count = 0
        while True:
            if output:
                self.weight = this
                self.log["cost"].append(self.cost())
                self.log["deviation"].append(self.deviation(
                    self.fprime(self.param, self.value, this)))
                self.log["gradient"].append(3 * count * self.limit)

            tmp = self.ternary(this) + prev * self.beta
            this = this + tmp
            prev = tmp
            count += 1

            if ((not precision is None) and precision >= train.umax(self.fprime(self.param, self.value, this))) \
                    or ((not cycles is None) and count >= cycles):
                break
        self.weight = this

    def ternary(self, prev):
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
        return origin * best

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
    
    @staticmethod
    def umax(x):    # recursively get the maximum of a ndarray
        if isinstance(x, np.float64) or isinstance(x, float):
            return abs(x)
        maxi = train.umax(x[0])
        for i in range(x.shape[0]):
            maxi = train.umax(x[i])
        return maxi
