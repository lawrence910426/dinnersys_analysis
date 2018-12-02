from dateutil.parser import parse
import datetime
import os
import numpy as np


class transfer_matrix:
    def __init__(self, orders ,dish_code):
        self.dishcode = dish_code

        usercount = {}
        for key in orders:
            row = orders[key]
            uid = row.seatno
            datetime = row.date.split(" ")[0]
            if usercount.setdefault(uid) is None:
                usercount[uid] = {}
            if usercount[uid].setdefault(datetime) is None:
                usercount[uid][datetime] = []
            usercount[uid][datetime].append(row)
        self.usercount = usercount

    def get_matrix(self):
        matrix = self.get_count()
        ret = np.zeros(matrix.shape, dtype=np.float)
        for i in range(matrix.shape[0]):
            sum = 0
            for j in range(matrix.shape[1]):
                sum += matrix[i, j]

            if sum == 0:
                ret[i, i] = 1       # means this dish would never transfer
            else:
                for j in range(matrix.shape[1]):
                    ret[j, i] = matrix[i, j] / sum
        return ret

    def get_count(self):
        adapt = self.dishcode

        summa = np.zeros((adapt.get_count(), adapt.get_count()), dtype=np.int)

        for uid in self.usercount:
            history = self.usercount[uid]

            # make history a sorted list.
            history = [(history[key]) for key in sorted(history.keys())]

            last = history[0]
            for data in history:
                if(last == data):  # if this is the first run.
                    continue
                summa += self.get_user_count(last, data)
                last = data
        return summa

    def get_user_count(self, last, data):

        # This will return a matrix ,which contains all combinations of last and data
        # ex. last = {1 ,3} ,data = {2 ,4}
        # tmp[1 ,2] = tmp[1 ,4] = tmp[3 ,2] = tmp[3 ,4] = 1
        # return tmp

        adapt = self.dishcode

        count = np.zeros((adapt.get_count(), adapt.get_count()), dtype=np.int)
        last_ids = []
        data_ids = []

        if(last == []):
            last_ids = [0]
        else:
            for row in last:
                last_ids.append(adapt.get_id(row.dish.name))

        if(data == []):
            data_ids = [0]
        else:
            for row in data:
                data_ids.append(adapt.get_id(row.dish.name))

        for i in last_ids:
            for j in data_ids:
                count[i, j] += 1
        return count


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