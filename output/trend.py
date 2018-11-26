import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import analysis.linear_regression as lg
import numpy as np


def trend(analysiser):
    result = analysiser.get_dish_date()
    balance = analysiser.get_balance()
    date ,dish = analysiser.get_decoders()

    for did in dish:
        index = [date[date_id] for date_id in date]
        value = [result[date_id, did] for date_id in date]

        dates = len(index)
        linear = lg.linear_regression([(i, value[i]) for i in range(dates)])

        balance_value = [balance[date_id ,did] for date_id in date]

        fig = plt.figure(1)
        plt.bar(index, value)
        plt.plot([0, dates], [linear.get(0), linear.get(dates)],
                 'C1', label=u'Linear regression', marker='o')
        plt.plot(range(dates), balance_value,
                 'C2', label=u'Model prediction', marker='o')
        fig.suptitle(dish[did])
        plt.legend()
        plt.show()
