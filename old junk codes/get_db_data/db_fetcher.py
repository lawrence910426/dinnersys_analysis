import MySQLdb
from get_db_data.dinnersys import dinnersys
import numpy as np
from datetime import datetime


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
        db = MySQLdb.connect("localhost", "root", "2rjurrru", "dinnersys")
        cursor = db.cursor()
        self.ds = dinnersys(cursor, datetime.strptime(l, "%Y-%m-%d"),
                       datetime.strptime(r, "%Y-%m-%d"))

    def get_person(self):
        return self.ds.get_row()
