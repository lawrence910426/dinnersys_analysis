import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import pickle

from analysis.logistic.logistic import *
from datetime import datetime
from datetime import timedelta
from get_db_data.db_fetcher import data_fetcher
from accuracy import accuracy
from marker import marker
from analysis.micro.booster import booster
from analysis.micro.decision import decision
import time

from tester import tester

segment = [
    ('2018-10-01', '2019-01-15')
]
for item in segment:
    start, end, list, index = item[0], item[1], [], []
    ostart, oend = datetime.strptime('2018-11-12', "%Y-%m-%d"), datetime.strptime('2018-12-21', "%Y-%m-%d")
    while ostart != oend:
        list.append(ostart.strftime("%Y-%m-%d"))
        index.append(ostart)
        ostart += timedelta(days=1)

    mark = tester({
        "cycles": 20,
        "limit": 5,
        "threads": 50
    }, start, end, list)
    is_trash = mark.is_trash()
    print("Accuracy:")
    print(np.sum(np.divide(np.abs(np.subtract(np.array(mark.real_value), np.array(mark.test_value))),
                           np.array(mark.test_value))))
    print("### Passed testing ###" if not is_trash else "Did not pass")

    # if not is_trash:
    plt.figure(num='Predict', figsize=(10, 10))
    plt.bar(index, mark.real_value)
    plt.plot(index, mark.test_value, color='orange')
    plt.show()
