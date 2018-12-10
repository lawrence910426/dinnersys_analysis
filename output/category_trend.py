import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *


def category_trend(orders):
    analysiser = analysis(orders, "exists")
    result = analysiser.get_dish_date()
    date, dish = analysiser.get_decoders()
    dates = len(date)
    balance = analysiser.get_balance(type="day_avg")

    for did in dish:
        index = [parse(date[date_id]) for date_id in date]
        value = [result[date_id, did] for date_id in date]

        balance_value = [balance[date_id, did] for date_id in date]

        formatter = date_format(index)
        fig, ax = plt.subplots()

        ax.xaxis.set_major_formatter(formatter)
        fig.autofmt_xdate()

        plt.bar(range(dates), value ,label="Original data")
        plt.plot(range(dates), balance_value, 'C1',
                 label='Stable state', marker='o')
        fig.suptitle(dish[did])

        plt.legend()
        plt.show()
