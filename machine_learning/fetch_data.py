import neuron_network
import MySQLdb
from dinnersys import dinnersys
import numpy as np
from dateutil.relativedelta import *
from datetime import datetime
from collections.abc import Iterable
import pandas as pd
import os


class data_fetcher:
    def __init__(self, l, r):
        self.user_id = ""
        self.user_class = ""
        self.hesistate = ""
        self.timestamp = ""
        self.year = ""
        self.month = ""
        self.day = ""
        self.weekday = ""

        self.gender = ""
        self.money = ""
        self.memorize = ""
        self.height = ""
        self.weight = ""
        self.location = ""
        self.virtue = ""

        self.pressure = ""
        self.temp = ""
        self.raining = ""
        self.cloud = ""
        self.humid = ""

        self.factory_no = ""
        self.load(l ,r)

    def load(self, l ,r):
        self.input, self.output = [], []
        db = MySQLdb.connect("localhost", "root", "2rjurrru", "dinnersys")
        cursor = db.cursor()
        ds = dinnersys(cursor, datetime.strptime(l, "%Y-%m-%d"),
                       datetime.strptime(r, "%Y-%m-%d"))
        while True:
            row = ds.get_row()
            if row == None:
                break
            self.input.append(row[0])
            self.output.append(row[1])

    def get_train(self):
        return np.array(self.input, dtype=np.float32), np.array(self.output, dtype=np.float32)
