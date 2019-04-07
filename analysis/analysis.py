from analysis.reencode.reencode_dish import *
from analysis.reencode.reencode_date import *
from analysis.matrix import *
from analysis.solve import *
from analysis.amount import *
import analysis.linear as lg
import numpy as np
import time


class analysis:
    def __init__(self, orders, style):
        self.data = orders
        self.dish_coder = reencode_dish()
        self.date_coder = reencode_date(orders, style)

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

    def get_decoders(self):
        return self.date_coder.decoder, self.dish_coder.decoder

    # -----------------------------------------------------------------------
    def init_balance(self):
        transfer, solver = transfer_matrix(orders, self.dish_coder), solve()
        self.matrix = transfer.get_count()
        self.balance = solver.get(transfer.get_matrix())

    def get_balance(self, **kwargs):
        if kwargs.setdefault("type") is None:
            return self.balance.T[0]

        if kwargs["type"] == "day_avg":
            date_count = np.zeros(
                (1, self.date_coder.get_count()), dtype=np.float)
            for oid in self.data:
                row = self.data[oid]
                date_count[0, self.date_coder.get_id(row.date)] += 1
            result = self.balance.dot(date_count)
            return result.T

        if kwargs["type"] == "linear":
            line = kwargs["line"]
            date_count = np.zeros(
                (1, self.date_coder.get_count()), dtype=np.float)
            for i in range(self.date_coder.get_count()):
                date_count[0, i] = line.get(i)
            result = self.balance.dot(date_count)
            return result.T

    def get_count_matrix(self):
        return self.matrix
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    def init_amount(self ,start ,end):
        self.amount = amount(self.data)

        def callback():
            self.amount_result = self.amount.get()
        self.amount_result = None
        self.amount.train(start ,end ,callback)

    def get_amount_result(self):
        while self.amount_result is None:
            time.sleep(1)
        return self.amount_result

    def get_amount(self):
        i, maxi = 0, 0
        for j in range(len(self.get_amount_result())):
            if maxi < self.amount_result[j]:
                i, maxi = j, self.amount_result[j]
        return i
    # -----------------------------------------------------------------------

    @staticmethod
    def get_linear(data):
        return lg.linear(data)
