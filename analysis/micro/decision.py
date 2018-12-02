from analysis.micro.neuron import *
import datetime
import time
from dateutil import parser
import copy

class decision:
    # input: previous order data for K days(including nothing)
    # output: whether he will order tomorrow

    def __init__(self, orders, param_len, uid):
        # input: order data (just for this person)
        # orders = {date:[order_1 ,order_2]}
        orders = copy.deepcopy(orders)
        self.orders, self.param_len = orders, param_len

        def exists(data, index):
            index = index.strftime("%Y-%m-%d")
            return 0 if data.setdefault(index) is None else 1

        mini, maxi, i = min(orders.keys()), max(orders.keys()), 0
        mini, maxi = parser.parse(mini), parser.parse(maxi)
        day_length = (maxi - mini).days + 1
        array_len = day_length - param_len if day_length - param_len > 0 else 0
        param = np.zeros((array_len, param_len))
        value = np.zeros((array_len, 1))

        mini += datetime.timedelta(days=param_len)

        while mini <= maxi:
            for j in range(param_len):
                param[i, j] = exists(orders, mini - datetime.timedelta(days=j+1))
            value[i] = exists(orders, mini)
            i += 1
            mini += datetime.timedelta(days=1)

        self.neuron = neuron(param, value, uid)
        self.exists, self.mini, self.maxi = exists, mini, maxi

    def train(self, booster, callback):
        booster.queue([self.neuron, callback])

    def get(self):
        param = [self.exists(self.orders, self.maxi - datetime.timedelta(days=i))
                 for i in range(self.param_len)]
        return self.neuron.get(np.array(param))
