import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *
from matplotlib.ticker import Formatter


def prediction(orders):
    analysiser = analysis(orders, "exists")
    date, dish = analysiser.get_decoders()
    result = analysiser.get_dish_date()

    space, width = 0.5, 0.1
    days = 3

    dishlen, datelen = len(dish), len(date)
    balance = analysiser.get_balance()
    amount = 300  # analysiser.get_amount()
    balance *= amount

    fig, ax = plt.subplots()

    i = 0
    for dt in range(datelen - days, datelen):
        plt.bar(np.arange(dishlen) + i * (dishlen + 1), [result[dt, i] for i in range(dishlen)],
                label="Day" + str(dt - datelen + days + 1))
        i += 1

    plt.bar(np.arange(dishlen) + i * (dishlen + 1), [balance[i] for i in range(dishlen)],
        label="Model prediction", color='white', edgecolor='black', hatch="/")
    
    fmt = dish_format(dish)
    ax.xaxis.set_major_formatter(fmt)

    tmp = []
    for j in range((dishlen + 1) * (days + 1)):
        if j % (dishlen + 1) != dishlen:
            tmp.append(j)
    plt.xticks(tmp)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()


class dish_format(Formatter):
    def __init__(self, decoder):
        self.decoder = decoder

    def __call__(self, x, pos=0):
        ind = int(np.round(x)) % (len(self.decoder) + 1)
        if self.decoder.setdefault(ind) is None:
            return ''
        else:
            return self.decoder[ind]