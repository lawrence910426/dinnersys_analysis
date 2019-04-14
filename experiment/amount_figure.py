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


def amount_figure(start, end, duration, location):
    real, model = [], {}

    data_all = fetch_data.load(location, '2000-01-01', '9999-12-01')

    data = fetch_data.get(data_all ,start ,end)
    analysiser = analysis(data, "weekdays")
    result = analysiser.get_dish_date()
    date, dish = analysiser.get_decoders()
    real = result.dot(np.array([1 for i in range(len(dish))]))

    def run(date):
        psuedo_start = (date -
                        datetime.timedelta(days=duration)).strftime("%Y-%m-%d")
        psuedo_end = date.strftime("%Y-%m-%d")
        data = fetch_data.get(data_all ,psuedo_start ,psuedo_end)
        analysiser = analysis(data, "weekdays")
        analysiser.init_amount(date - datetime.timedelta(days=duration),
                               date + datetime.timedelta(days=1))
        model[date + datetime.timedelta(days=1)] = analysiser.get_amount()

    start, end = parse(start), parse(end)
    real_start = start
    start += datetime.timedelta(days=duration)
    while start <= end:
        run(start)
        start += datetime.timedelta(days=1)
        print(start, model[start] ,datetime.datetime.now())

    with open("experiment_output\\" +
              real_start.strftime("%Y-%m-%d") + '_' +
              end.strftime("%Y-%m-%d") + '_' +
              str(duration) + '.csv', 'a') as the_file:
        for i in range(len(date) + 1):
            r = real[i] if i in real else '-'
            m = model[real_start + datetime.timedelta(
                days=i)] if real_start + datetime.timedelta(days=i) in model else '-'
            d = date[i] if i in date else '-'
            the_file.write(d + "," + str(r) + "," + str(m) + '\n')

    formatter = date_format([parse(date[i]) for i in date])
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)
    # plt.xticks(np.arange(0 ,dates ,1))

    plt.bar(range(duration, len(date)),
            [real[i] for i in range(duration, len(date))])
    plt.plot(range(duration + 1, len(date) + 1),
             [model[real_start + datetime.timedelta(days=i)]
              for i in range(duration + 1, len(date) + 1)],
             'C1', label=u'Model', marker='o')
    plt.show()
