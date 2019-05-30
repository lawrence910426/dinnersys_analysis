from analysis.micro.neuron import *
import datetime
import time
from dateutil import parser
import copy
import numpy as np

class decision:
    # input: previous order data for K days(including nothing)
    # output: whether he will order tomorrow
    def __init__(self, param ,value ,code):
        # input: order data (just for this person)
        # orders = {date:[order_1 ,order_2]}
        self.neuron = neuron(param, value, code)

    def train(self, booster, callback):
        booster.queue([self.neuron, callback])

    def get(self ,param):
        return self.neuron.get(np.array(param))
