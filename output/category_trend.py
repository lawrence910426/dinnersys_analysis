import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *


def category_trend(orders):
    analysiser = analysis(orders ,"exists")
    result = analysiser.get_dish_date()
    date ,dish = analysiser.get_decoders()
    dates = len(date)
    linear = analysis.get_linear([(i, sum(result[i])) for i in range(dates)])
    balance = analysiser.get_balance(line=linear ,linear=True)

    for did in dish:
        index = [parse(date[date_id]) for date_id in date]
        value = [result[date_id, did] for date_id in date]

        balance_value = [balance[date_id ,did] for date_id in date]

        formatter = date_format(index)
        fig, ax = plt.subplots()

        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(np.arange(0 ,dates ,1))
        
        plt.bar(range(dates), value)
        plt.plot(range(dates), balance_value,
                 'C2', label=u'Model prediction', marker='o')
        fig.suptitle(dish[did])
        plt.show()
