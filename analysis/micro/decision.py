from analysis.micro.neuron import *
import datetime
import time
from dateutil import parser
import copy
import numpy as np

class decision:
    # input: previous order data for K days(including nothing)
    # output: whether he will order tomorrow

    def __init__(self, orders, start ,end, uid):
        # input: order data (just for this person)
        # orders = {date:[order_1 ,order_2]}
        orders = copy.deepcopy(orders)
        self.orders = orders

        def exists(data, index):
            index = index.strftime("%Y-%m-%d")
            return 0 if data.setdefault(index) is None else 1
        
        param = np.zeros(((end - start).days + 1 ,7))
        value = np.zeros(((end - start).days + 1, 1))
        i = 0

        while start <= end:
            param[i, start.weekday()] = True
            value[i] = exists(orders, start)
            i += 1
            start += datetime.timedelta(days=1)
        
        self.neuron = neuron(param, value, uid)

    def train(self, booster, callback):
        booster.queue([self.neuron, callback])

    def get(self ,date):
        param = [date.weekday() == i for i in range(7)]
        return self.neuron.get(np.array(param))
