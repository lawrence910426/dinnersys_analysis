import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *

def sum_trend(data):
    analysiser = analysis(data ,"weekdays")
    result = analysiser.get_dish_date()
    date, dish = analysiser.get_decoders()
    result = result.dot(np.array([1 for i in range(len(dish))]))

    index = [parse(date[date_id]) for date_id in date]
    value = [result[date_id] for date_id in date]

    dates = len(index)
    linear = analysis.get_linear([(i, value[i]) for i in range(dates)])

    formatter = date_format(index)

    fig, ax = plt.subplots()

    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(np.arange(0 ,dates ,1))
    plt.bar(range(dates), value)
    plt.plot([0, dates], [linear.get(0), linear.get(dates)],
             'C1', label=u'Linear regression', marker='o')
    plt.show()
