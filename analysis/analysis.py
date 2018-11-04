from analysis.reencode_dish import *
from analysis.transfer_matrix import *
from analysis.solve_matrix import *
import numpy as np


class analysis:
    def __init__(self, orders):
        self.data = orders
        self.coder = reencode_dish()
        transfer = transfer_matrix(orders)
        solver = solve_matrix()
        self.matrix = transfer.get_count()
        self.balance = solver.solve(transfer.get_matrix())

    def get_count(self):
        return len(self.data)

    def get_dish(self ,mode):
        ret = {}
        for oid in self.data:
            item = self.data[oid]
            did = self.coder.get_id(item.dish.name)
            if(ret.setdefault(did) is None):
                ret[did] = 0
            ret[did] += 1

        if mode == "percent":
            for key in ret:
                ret[key] /= self.get_count()
        
        index = [self.coder.get_name(key) for key in ret]
        value = [ret[key] for key in ret]
        return index ,value

    def get_class(self ,mode):
        ret = {}
        for oid in self.data:
            item = self.data[oid]
            if ret.setdefault(item.seatno[:3]) is None:
                ret[item.seatno[:3]] = 0
            ret[item.seatno[:3]] += 1

        if mode == "percent":
            for key in ret:
                ret[key] /= self.get_count()
        
        index = [seat for seat in sorted(ret.keys())]
        value = [ret[seat] for seat in sorted(ret.keys())]
        return index ,value

    def get_date(self ,mode):
        ret = {}
        for oid in self.data:
            item = self.data[oid]
            if ret.setdefault(item.date) is None:
                ret[item.date] = 0
            ret[item.date] += 1

        if mode == "percent":
            for key in ret:
                ret[key] /= self.get_count()
        
        index = [date[5:].replace("-" ,"") for date in ret]
        value = [ret[date] for date in ret]
        return index ,value

    def get_balance_matrix(self, mode):
        ret = np.copy(self.balance)
        size = ret.shape[0]

        if mode == "rounded":
            ret *= self.get_count()
            ret = np.array(np.around(ret), dtype=np.int)

        if mode == "estimate":
            ret *= self.get_count()

        index = [self.coder.get_name(idx) for idx in range(size)]
        value = [ret[idx][0] for idx in range(size)]
        return index, value

    def get_count_matrix(self):
        return self.matrix
