import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle

'''
from experiment.sum_trend import *
from experiment.amount_figure import *
from experiment.algorithm_compare import *
from output.category_trend import *
from output.prediction import *
'''

from analysis.logistic.logistic import *
from datetime import datetime
from get_db_data.db_fetcher import data_fetcher
from accuracy import accuracy
from marker import marker
from analysis.micro.booster import booster
from analysis.micro.decision import decision
import time

done, require = 0, 0
def tester(boost_conf ,start ,end ,test):
    global done
    global require
    done, require = 0, 0

    def callback(uid):
        global done
        global require
        done += 1
        print("done training on {} ,total {} was done ,requires {}.".format(uid, done, require))

    df = data_fetcher(start, end)
    stamp = lambda x: datetime.strptime(x, "%Y-%m-%d").timestamp()

    deciders = []
    boost = booster(boost_conf)

    test = [(stamp(item) - stamp(start)) / (stamp(end) - stamp(start)) for item in test]
    while True:
        data = df.get_person()
        if data is None:
            break

        accu = accuracy(data[0], data[1], test)
        run_data = accu.get_run()
        dec = decision(run_data[0], run_data[1], data[2])
        deciders.append([dec, accu])
        require += 1

    for item in deciders:
        item[0].train(boost, callback)

    while require != done:
        time.sleep(1)

    entity = {
        "data": {
            "test_input": [],
            "test_output": [],
            "test_query": []
        }
    }
    for item in deciders:
        dec, accu = item[0], item[1]
        # print(dec.neuron.loaded["function"].log["cost"])
        test_in, test_out = accu.get_test()
        for i in range(test_in.shape[0]):
            q = dec.get(test_in[i])
            entity["data"]["test_input"].append(test_in[i])
            entity["data"]["test_output"].append(test_out[i])
            entity["data"]["test_query"].append(q)

    return  marker(entity)
