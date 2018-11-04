import numpy as np
import pandas as pd

import pandas as pd


class solve_matrix:

    def solve(self, matrix):
        for i in range(matrix.shape[0]):
            matrix[i, i] -= 1

        # remove any line ,because one of them is useless.
        matrix[matrix.shape[0] - 1, :] = 1
        
        inv = np.linalg.inv(matrix)

        target = np.zeros((matrix.shape[0], 1), dtype=np.float)
        target[matrix.shape[0] - 1, 0] = 1

        return inv.dot(target)
