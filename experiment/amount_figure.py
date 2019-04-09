import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *
from internet_data.fetch_data import *
import json


def amount_figure(start, end, duration):
    real, model = [], {}

    data = fetch_data.load("data_local.pickle", start, end)
    analysiser = analysis(data, "weekdays")
    result = analysiser.get_dish_date()
    date, dish = analysiser.get_decoders()
    real = result.dot(np.array([1 for i in range(len(dish))]))

    def run(date):
        psuedo_start = (date -
                        datetime.timedelta(days=duration)).strftime("%Y-%m-%d")
        psuedo_end = date.strftime("%Y-%m-%d")
        data = fetch_data.load("data_local.pickle", psuedo_start, psuedo_end)
        analysiser = analysis(data, "weekdays")
        analysiser.init_amount(date - datetime.timedelta(days=duration),
                               date + datetime.timedelta(days=1))
        model[date + datetime.timedelta(days=1)] = analysiser.get_amount()
        print(date)

    start, end = parse(start), parse(end)
    real_start = start
    start += datetime.timedelta(days=duration)
    while start <= end:
        run(start)
        start += datetime.timedelta(days=1)

    with open(start.strftime("%Y-%m-%d") + '_' +
              end.strftime("%Y-%m-%d") + '_' +
              str(duration) + '.csv', 'a') as the_file:
        for i in range(len(date)):
            if i > duration:
                the_file.write(date[i] + "," + str(real[i]) + "," +
                               str(model[real_start + datetime.timedelta(days=i)]) + '\n')
            else:
                the_file.write(date[i] + "," + str(real[i]) + '\n')

    formatter = date_format([parse(date[i]) for i in date])
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)
    # plt.xticks(np.arange(0 ,dates ,1))
    plt.bar(range(duration + 1, len(date)), real)
    plt.plot(range(duration + 1, len(date) + 1),
             [model[real_start + datetime.timedelta(days=i)]
              for i in range(duration + 1, len(date) + 1)],
             'C1', label=u'Model', marker='o')
    plt.show()
