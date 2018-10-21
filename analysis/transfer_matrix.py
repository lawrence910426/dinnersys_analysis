from analysis.reencode_dish import *
from data_structure.order import *
from dateutil.parser import parse
import datetime
import os
import numpy as np


class transfer_matrix:
    def __init__(self, orders):
        self.dishcode = reencode_dish(orders)

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

    def get_matrix(self, start, end):
        start = parse(start)
        end = parse(end)

        adapt = self.dishcode
        summa = np.zeros(
            (adapt.get_count() + 1, adapt.get_count() + 1), dtype=np.int)

        for uid in self.usercount:
            history = self.usercount[uid]
            current = start + datetime.timedelta(days=1)
            last = history.setdefault(str(current.date()))
            last = [] if last is None else last

            while current != end:
                data = history.setdefault(str(current.date()))
                data = [] if data is None else data

                summa += self.get_count_matrix(last, data)

                last = data
                current += datetime.timedelta(days=1)
        return summa

    def get_count_matrix(self, last, data):
        adapt = self.dishcode
        count = np.zeros(
            (adapt.get_count() + 1, adapt.get_count() + 1), dtype=np.int)
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
