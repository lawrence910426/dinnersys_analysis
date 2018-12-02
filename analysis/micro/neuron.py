from analysis.logistic import *


class neuron:
    def __init__(self, params, value, nid=-1):
        self.model = []
        self.param = params
        self.value = value
        self.nid = nid

    def build(self, step, cycle, precision):
        lo = logistic(self.param, self.value)
        lo.train(step=step, cycles=cycle, precision=precision, output=False)

        fails = 0
        for i in range(len(self.param)):
            model_v = lo.query(self.param[i])
            real_v = self.value[i]
            fails += 1 if (model_v > 0.5 and real_v <
                           0.5) or (model_v < 0.5 and real_v > 0.5) else 0

        package = {"fails": fails, "samples": len(self.param), "step": step,
                   "precision": precision, "cycle": cycle, "function": lo}
        self.model.append(package)

    def load(self):
        idx, mini = 0, self.model[0]["fails"]
        for i in range(len(self.model)):
            if self.model[i]["fails"] < mini:
                idx, mini = i, self.model[i]["fails"]
        self.loaded = self.model[idx]
        self.model = [self.loaded]      # clear junk
        return self.nid

    def get(self, param):
        return self.loaded["function"].query(param)
