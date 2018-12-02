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

        decisions, networks = {}, {}

        for u in array.keys():
            decisions[u] = decision(array[u], self.param["param_len"], u)
            networks[u] = network(array[u], dish_code, u)

        self.decision, self.network, self.boost = decisions, networks, boost
        self.array, self.undone, self.dish_code = array, 0, dish_code

    def train(self, uid, callback):
        self.callback = callback
        self.decision[uid].train(self.boost, self.done_decision)

    def done_decision(self, uid):
        self.network[uid].train(self.boost, self.done_network)

    def done_network(self, uid):
        self.callback(uid)

    def get(self, uid):
        potential = self.network[uid].get()
        decision = self.decision[uid].get()
        netowrk_model = dict(
            (
                self.dish_code.get_name(key), {
                    "fails": self.network[uid].neuron[key].loaded["fails"],
                    "samples": self.network[uid].neuron[key].loaded["samples"],
                    "step": self.network[uid].neuron[key].loaded["step"],
                    "precision": self.network[uid].neuron[key].loaded["precision"],
                    "cycle": self.network[uid].neuron[key].loaded["cycle"]
                }
            ) for key in self.network[uid].neuron.keys()
        )

        decision_model = {
            "fails": self.decision[uid].neuron.loaded["fails"],
            "samples": self.decision[uid].neuron.loaded["samples"],
            "step": self.decision[uid].neuron.loaded["step"],
            "precision": self.decision[uid].neuron.loaded["precision"],
            "cycle": self.decision[uid].neuron.loaded["cycle"]
        }
        return {"user id": uid,
                "network model": netowrk_model,
                "decision model": decision_model,
                "potentials": potential,
                "decision": decision}
