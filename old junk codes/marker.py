from scipy.stats import chisquare
import math
import numpy as np


class marker:
    def __init__(self, entity):
        self.entity = entity

    def chi_square(self):
        real_value, test_value = {}, {}
        for i in range(len(self.entity["data"]["test_input"])):
            timestamp = self.entity["data"]["test_input"][i][0]
            if real_value.setdefault(timestamp) is None:
                real_value[timestamp] = 0
            real_value[timestamp] += self.entity["data"]["test_output"][i][0]
            if test_value.setdefault(timestamp) is None:
                test_value[timestamp] = 0
            test_value[timestamp] += self.entity["data"]["test_query"][i]

        real_value = [real_value[key] for key in sorted(real_value.keys())]
        test_value = [test_value[key] + 1e-6 for key in sorted(test_value.keys())]
        self.real_value, self.test_value = real_value, test_value
        return chisquare(real_value, f_exp=test_value)

    # def KL_Divergence(self):

    def is_trash(self):
        chi_value, p_value = self.chi_square()
        print("chi_value:{} ,p_value:{}".format(chi_value, p_value))
        return np.isnan(p_value) or p_value < 0.01 or chi_value < 1e-4
