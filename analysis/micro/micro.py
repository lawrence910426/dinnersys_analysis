from analysis.micro.decision import *
from analysis.micro.network import *
from analysis.micro.booster import *
from analysis.reencode.reencode_dish import *


class micro:
    # input: orders
    # output: how much orders would be tomorrow
    param = {
        "param_len": 7
    }

    def __init__(self, orders):
        array = {}
        for k in orders.keys():
            order = orders[k]
            uid = order.seatno
            date = order.date
            if array.setdefault(uid) is None:
                array[uid] = {}
            if array[uid].setdefault(date) is None:
                array[uid][date] = []
            array[uid][date].append(order)

        dish_code = reencode_dish()
        boost = booster()

        self.decision, self.network, self.boost, self.array = {}, {}, boost, array
        self.array, self.undone, self.dish_code = array, 0, dish_code

    def train(self, uid, callback):
        self.decision[uid] = decision(
            self.array[uid], self.param["param_len"], uid)
        # self.network[uid] = network(self.array[uid], self.dish_code, uid)
        self.callback = callback
        self.decision[uid].train(self.boost, self.done)

    # def done_decision(self, uid):
    #     self.network[uid].train(self.boost, self.done_network)

    def done(self, uid):
        self.callback(uid)

    def get(self, uid):
        decision = self.decision[uid].get()

        decision_model = {
            "cost": self.decision[uid].neuron.loaded["cost"],
            "samples": self.decision[uid].neuron.loaded["samples"],
            "step": self.decision[uid].neuron.loaded["step"],
            "precision": self.decision[uid].neuron.loaded["precision"],
            "cycle": self.decision[uid].neuron.loaded["cycle"]
        }
        return {"user id": uid,
                "model": decision_model,
                "rate": decision}
