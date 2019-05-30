from scipy.stats import chisquare
import math
import numpy as np


class marker:
    def __init__(self, entity):
        self.entity = entity
    '''
    "show": {
        "path": path,
        "neuron_type": self.neuron_type,
        "batch": self.batch,
        "step": self.step,
        "learning_rate": self.learning_rate,
        "momentum": self.momentum,
        "real_accuracy": real_mse,
        "test_accuracy": test_mse,
        "loss": n.loss(sess)
    },
    "data": {
        "real_query": real_query,
        "test_input": test_in,
        "test_output": test_out,
        "test_query": test_query,
    }
    '''
    def is_overfitting(self):
        return abs(self.entity["show"]["real_accuracy"] - self.entity["show"]["test_accuracy"]) > 0.2

    def chi_square(self):
        real_value, test_value = {}, {}
        for i in range(len(self.entity["data"]["test_input"])):
            timestamp = math.floor(self.entity["data"]["test_input"][i][0] / 86400)
            if real_value.setdefault(timestamp) is None:
                real_value[timestamp] = 0
            real_value[timestamp] += (1 if self.entity["data"]["test_output"][i][0] else 0)
            if test_value.setdefault(timestamp) is None:
                test_value[timestamp] = 0
            test_value[timestamp] += self.entity["data"]["test_query"][i][0]

        real_value = [real_value[key] for key in sorted(real_value.keys())]
        test_value = [test_value[key] + 1e-6 for key in sorted(test_value.keys())]
        print("Real_list ,Test_list:", real_value, test_value)
        return chisquare(real_value, f_exp=test_value)

    # def KL_Divergence(self):

    def is_trash(self):
        chi_value, p_value = self.chi_square()
        overfit = self.is_overfitting()
        print("checker:", overfit, chi_value, p_value)
        return np.isnan(p_value) or p_value > 0.01 or overfit or chi_value < 1e-4
