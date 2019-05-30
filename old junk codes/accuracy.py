import numpy as np
import os
import time
import gc

class accuracy:
    def __init__(self ,input ,output ,test_cases):
        test_in ,test_out = [] ,[]
        run_in ,run_out = [] ,[]

        for i in range(input.shape[0]):
            if input[i][0] in test_cases:
                test_in.append(input[i])
                test_out.append(output[i])
                run_in.append(input[i])
                run_out.append(output[i])

            else:
                run_in.append(input[i])
                run_out.append(output[i])

        self.test_in ,self.test_out = np.array(test_in, dtype=np.float32) ,np.array(test_out, dtype=np.float32)
        self.input ,self.output = np.array(run_in, dtype=np.float32) ,np.array(run_out, dtype=np.float32)



    def get_test(self):
        return self.test_in ,self.test_out

    def get_run(self):
        return self.input ,self.output

    def get_accuracy(self ,target ,output):     # Mean Squared Error
        wrongs = 0
        for i in range(target.shape[0]):
            for j in range(target.shape[1]):
                wrongs += (target[i][j] - output[i][j]) ** 2
        return wrongs / target.shape[0]