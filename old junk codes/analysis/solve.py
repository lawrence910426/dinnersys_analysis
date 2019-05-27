import numpy as np
import random

class solve:

    param = {
        "min": 10 ** 7,
        "max": 10 ** 10,
        "samples": 10 ** 3
    }

    def get(self, matrix):
        try:
            return self.solve(matrix)
        except:
            return self.exp_square(matrix)

    def solve(self, matrix):
        for i in range(matrix.shape[0]):
            matrix[i, i] -= 1

        # remove any line ,because one of them is useless.
        matrix[matrix.shape[0] - 1, :] = 1

        inv = np.linalg.inv(matrix)

        target = np.zeros((matrix.shape[0], 1), dtype=np.float)
        target[matrix.shape[0] - 1, 0] = 1

        return inv.dot(target)

    def exp_square(self, matrix):
        size = matrix.shape[0]
        result = np.zeros((size), dtype=np.float)

        for i in range(self.param["samples"]):
            vector = np.array([1 / size for i in range(size)])

            ans = matrix
            tmp = matrix

            rand = (random.random() +
                    self.param["min"]) * (self.param["max"] / self.param["min"])
            rand = int(rand)
            while rand != 0:
                tmp = tmp.dot(tmp)
                if rand % 2 == 1:
                    ans *= tmp
                rand = int(rand / 2)

            vector = vector.dot(ans)
            result += vector

        result /= self.param["samples"]
        return result
