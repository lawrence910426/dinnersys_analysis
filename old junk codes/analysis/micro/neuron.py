from analysis.logistic.logistic import *
import math
import os


class neuron:
    def __init__(self, params, value, nid=-1):
        self.model = []
        self.param = params
        self.value = value
        self.nid = nid

    def build(self, limit, cycle):
        lo = logistic(self.param, self.value)
        lo.train(limit=limit, cycles=cycle,
                 function="train_ternary", output=True)

        package = {"cost": lo.cost(), "samples": len(self.param),
                   "cycle": cycle, "function": lo}
        self.model.append(package)

    def load(self):
        idx, maxi = 0, self.model[0]["cost"]
        for i in range(len(self.model)):
            if self.model[i]["cost"] > maxi:
                idx, maxi = i, self.model[i]["cost"]
        self.loaded = self.model[idx]
        self.model = [self.loaded]      # clear junk
        return self.nid

    def get(self, param):
        # print(self.param, self.value ,self.loaded["function"].weight ,param ,self.loaded["function"].cost() ,self.loaded["function"].query(param))
        return self.loaded["function"].query(param)
