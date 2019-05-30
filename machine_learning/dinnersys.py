import os
from datetime import datetime
import time
from dateutil.relativedelta import *
import MySQLdb
import math


class dinnersys:
    def __init__(self, cursor, start, end):
        sql = """SELECT
            O.id ,U.id ,C.id ,F.id ,LO.esti_recv_datetime

            FROM orders AS O
            INNER JOIN users AS U 				ON O.user_id = U.id
            INNER JOIN user_information AS UI 	ON U.info_id = UI.id
            INNER JOIN class AS C				ON U.class_id = C.id
            INNER JOIN buffet AS BF				ON BF.order = O.id
            INNER JOIN dish AS D				ON BF.dish = D.id
            INNER JOIN department AS DP			ON D.department_id = DP.id
            INNER JOIN factory AS F				ON DP.factory = F.id
            INNER JOIN logistics_info AS LO		ON O.logistics_id = LO.id
            INNER JOIN money_info AS MI			ON O.money_id = MI.id
            INNER JOIN payment AS P 			ON P.money_info = MI.id AND (P.tag = 'cafeteria' OR P.tag = 'payment')

            WHERE O.disabled = FALSE AND P.paid"""
        cursor.execute(sql)
        self.orders = cursor.fetchall()

        self.category, self.person, self.class_no, self.factory, self.p2c = {}, {}, {}, {}, {}
        for row in self.orders:
            tmp = row[4].strftime("%Y-%m-%d")
            self.person[row[1]] = 1
            self.class_no[row[2]] = 1
            self.factory[row[3]] = 1
            self.p2c[row[1]] = row[2]

            if self.category.setdefault(tmp) is None:
                self.category[tmp] = {}
            if self.category[tmp].setdefault(row[1]) is None:
                self.category[tmp][row[1]] = []
            self.category[tmp][row[1]].append(row)

        self.one_hot()
        self.build_buffer(start, end)

    def one_hot(self):
        person = [[1 if i == j else 0 for j in self.person.keys()]
                  for i in self.person.keys()]
        class_no = [[1 if i == j else 0 for j in self.class_no.keys()]
                    for i in self.class_no.keys()]
        factory = [[1 if i == j else 0 for j in self.factory.keys()]
                   for i in self.factory.keys()]

        count = 0
        for i in self.person.keys():
            self.person[i] = person[count]
            count += 1

        count = 0
        for i in self.class_no.keys():
            self.class_no[i] = class_no[count]
            count += 1

        count = 0
        for i in self.factory.keys():
            self.factory[i] = factory[count]
            count += 1

    def build_buffer(self, start, end):
        self.ptr, self.buffer = 0, []
        while start != end:
            for key in self.person.keys():
                start_s = start.strftime("%Y-%m-%d")
                '''input = self.flatten([
                    start.timestamp(),  # start.year, start.month, start.day,
                    # [1 if i == start.month else 0 for i in range(12)],
                    # [1 if i == start.day else 0 for i in range(31)],
                    [[1 if i == start.weekday() and j == 1 else 0 for i in range(7)] for j in self.class_no[self.p2c[key]]],
                    # self.person[key] ,self.class_no[self.p2c[key]], 0,
                ])'''
                input = [1 if i == start.weekday() and j == 1 else 0 for i in range(7) for j in self.person[key]]
                input.insert(0 ,start.timestamp())
                if self.category.setdefault(start_s) is None or self.category[start_s].setdefault(key) is None:
                    self.buffer.append((input, [0]))
                else:
                    self.buffer.append((input, [1]))

            start += relativedelta(days=1)

    def get_row(self):
        ret = None if self.ptr == len(self.buffer) else self.buffer[self.ptr]
        self.ptr += 1
        return ret

    def flatten(self, data):
        ret = []
        for item in data:
            if type(item) == list:
                result = self.flatten(item)
                for r in result:
                    ret.append(r)
            else:
                ret.append(item)
        return ret

