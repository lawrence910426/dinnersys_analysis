from analysis.micro.decision import *
from analysis.micro.booster import *
from analysis.reencode.reencode_dish import *
import numpy as np
import os
from fractions import Fraction

class amount:
    # input: orders
    # output: how much orders would be tomorrow
    length = 7

    def __init__(self, orders):
        array = {}
        for k in orders.keys():
            order = orders[k]
            uid = order.seatno
            date = order.date
            if array.setdefault(uid) is None:
                array[uid] = {}
            if array[uid].setdefault(date) is None:
                array[uid][date] = []
            array[uid][date].append(order)

        boost = booster()

        self.decision, self.boost, self.array = {}, boost, array
        self.array, self.undone = array, 0

    def train(self, callback):
        self.callback = callback
        self.undone = len(self.array)
        for uid in self.array:
            if len(self.array[uid]) < self.length:
                self.undone -= 1
                continue

            self.decision[uid] = decision(self.array[uid], self.length, uid)
            self.decision[uid].train(self.boost, self.done)

    def done(self, uid):
        self.undone = self.undone - 1
        if self.undone == 0:
            self.rate = self.get_rate()
            self.callback()

    def get_rate(self):
        prev = np.zeros((len(self.array)) ,dtype=np.float64)
        rate = np.zeros((len(self.array)) ,dtype=np.float64)

        i = 0
        for uid in self.decision:
            p = self.decision[uid].get()

            for j in range(i + 1):
                rate[j] += prev[j] * (1 - p)
                rate[j + 1] = prev[j] * p

            if i == 0:
                rate[0] = 1 - p
                rate[1] = p

            prev = rate
            rate = np.zeros((len(self.array)) ,dtype=np.float64)
            i += 1
        return prev

    def get(self):
        return self.rate
