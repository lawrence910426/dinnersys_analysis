from analysis.reencode.reencode_dish import *
from analysis.reencode.reencode_date import *
from analysis.matrix import *
import analysis.linear as lg
import numpy as np


class analysis:
    def __init__(self, orders ,style):
        self.data = orders
        self.dish_coder = reencode_dish()
        self.date_coder = reencode_date(orders ,style)
        transfer ,solver = transfer_matrix(orders ,self.dish_coder) ,solve_matrix()
        self.matrix = transfer.get_count()
        self.balance = solver.solve(transfer.get_matrix())

    def get_count(self):
        return len(self.data)

    def get_dish_date(self):
        result = np.zeros((self.date_coder.get_count(),
                           self.dish_coder.get_count()), dtype=np.int)

        for oid in self.data:
            date = self.date_coder.get_id(self.data[oid].date)
            dish = self.dish_coder.get_id(self.data[oid].dish.name)
            result[date, dish] += 1

        return result

    def get_balance(self ,**kwargs):
        if not kwargs.setdefault("day_avg") is None:
            date_count = np.zeros((1, self.date_coder.get_count()), dtype=np.float)
            for oid in self.data:
                row = self.data[oid]
                date_count[0, self.date_coder.get_id(row.date)] += 1
            result = self.balance.dot(date_count)

        if not kwargs.setdefault("linear") is None:
            line = kwargs["line"]
            date_count = np.zeros((1, self.date_coder.get_count()), dtype=np.float)
            for i in range(self.date_coder.get_count()):
                date_count[0, i] = line.get(i)
            result = self.balance.dot(date_count)

        ret = np.zeros((result.shape[1] ,result.shape[0]) ,dtype=np.float)
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                ret[j ,i] = result[i ,j]
        return ret

    def get_decoders(self):
        dish_idx = dict((i, self.dish_coder.get_name(i))
                        for i in range(self.dish_coder.get_count()))
        return self.date_coder.decoder ,dish_idx

    def get_count_matrix(self):
        return self.matrix
    
    @staticmethod
    def get_linear(data):
        return lg.linear(data)
