from analysis.logistic import *
import math

class neuron:
    def __init__(self, params, value, nid=-1):
        self.model = []
        self.param = params
        self.value = value
        self.nid = nid

    def build(self, step, cycle, precision):
        lo = logistic(self.param, self.value)
        lo.train(step=step, cycles=cycle, precision=precision, output=True)

        package = {"cost": lo.cost(), "samples": len(self.param), "step": step,
                   "precision": precision, "cycle": cycle, "function": lo}
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
        return self.loaded["function"].query(param)
