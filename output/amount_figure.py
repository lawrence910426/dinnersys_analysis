import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from output.date_formatter import date_format
from dateutil.parser import parse
from analysis.analysis import *


def amount_figure(data):
    analysiser = analysis(data, "exists")
    result = analysiser.get_amount_result()
    length = len(result)

    summa, center, maxi, dist = 0, 0, 0, 0
    for i in range(length):
        if maxi < result[i]:
            center, maxi = i, result[i]
    
    while summa < 0.68:
        summa += result[center + dist] + result[center - dist]
        dist += 1

    plt.bar(range(length), [result[i] for i in range(length)])
    plt.show()

    while summa < 0.95:
        plt.bar(range(length), [result[i] for i in range(length)])
        for i in range(center - dist ,center + dist):
            plt.bar(i, result[i], color='red', edgecolor='red')
        plt.title("Distance: " + str(dist) + ",Rate: " + str(summa * 100) + "%")
        plt.show()

        summa += result[center + dist] + result[center - dist]
        dist += 1
