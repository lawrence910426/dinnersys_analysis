from analysis.micro.neuron import *
import datetime
import os


class network:
    # input {date:[orders]}
    # output {"noodles":87% ,"pots":72%}
    def __init__(self, orders, dish_code, uid):
        self.uid, self.dish_code = uid, dish_code
        param, value = {}, {}
        count = np.zeros(dish_code.get_count())

        def same(did, order):
            return 1 if did == self.dish_code.get_id(order.dish.name) else 0

        def append(data, key, item):
            if data.setdefault(key) is None:
                data[key] = []
            data[key].append(item)

        def access(data, key): return [] if data.setdefault(
            key) is None else data[key]

        yesterday, today = None, None
        for k in sorted(orders.keys()):
            today = orders[k]
            if not yesterday is None:
                for yest in yesterday:
                    for tod in today:
                        for did in range(dish_code.get_count()):
                            tmp = np.zeros(count.shape[0] + 1)
                            tmp[-1] = same(did, yest)
                            tmp[:-1] = count
                            append(param, did, tmp)
                            append(value, did, same(did, tod))

            yesterday = today
            for o in today:
                count[dish_code.get_id(o.dish.name)] += 1

        neurons = {}
        for did in range(dish_code.get_count()):
            neurons[did] = neuron(np.array(access(param, did)),
                                  np.array(access(value, did)), did)
        self.neuron = neurons
        self.count, self.today, self.same = count, today, same

    def train(self, booster, callback):
        self.callback = callback
        self.finished = {}
        for did in range(self.dish_code.get_count()):
            booster.queue([self.neuron[did], self.done])
            self.finished[did] = False

    def done(self, nid):
        flag = True
        self.finished[nid] = True
        for did in range(self.dish_code.get_count()):
            flag = flag and self.finished[did]
        if flag:
            self.callback(self.uid)

    def get(self):
        result = {}
        for did in range(self.dish_code.get_count()):
            tmp = 0
            for tod in self.today:
                param = np.zeros(len(self.count) + 1)
                param[:-1] = self.count
                param[-1] = self.same(did, tod)
                tmp += self.neuron[did].get(param)
            tmp /= len(self.today)
            result[self.dish_code.get_name(did)] = tmp
        return result
