import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *


def prediction(orders):
    analysiser = analysis(orders, "exists")
    date, dish = analysiser.get_decoders()
    length = len(dish)
    balance = analysiser.get_balance()
    amount = analysiser.get_amount()
    balance *= amount

    fig, ax = plt.subplots()

    plt.bar([dish[i] for i in range(length)], [balance[i] for i in range(length)],
            label="Model prediction", color='white', edgecolor='black', hatch="/")

    plt.legend()
    plt.show()
