from fetch_data import data_fetcher
from neuron_network import neuron_network
import tensorflow as tf
from accuracy import accuracy
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from marker import marker
from datetime import datetime
import math
import pprint
import gc


class genetic:

    def __init__(self, arg):
        self.learning_rate = 1e-4
        self.momentum = 0.9
        self.algorithm = tf.train.MomentumOptimizer(learning_rate=self.learning_rate
                                                    , momentum=self.momentum)
        self.neuron_type = [300, 200, 100]
        self.batch = 5000
        self.step = 1000

        for k in arg.keys():  # yeah fuck you i am just a lazy bitch
            exec("self.{} = arg[k]".format(str(k)))

        self.entity = None

    def merge(self, genetics):
        return genetics[0]

    def rank(self):
        mark = marker(self.entity)
        return mark.is_trash()

    def grow(self, accu, sess):
        test_in, test_out = accu.get_test()
        print("1")
        run_in, run_out = accu.get_run()
        print("2")
        n = neuron_network(
            run_in,
            self.neuron_type,
            run_out,
            self.algorithm(learning_rate=self.learning_rate, momentum=self.momentum),
            self.batch
        )
        print("3")
        n.train(sess, self.step)
        print("4")
        loss = n.loss(sess)
        print("5")
        test_query, test_mse = n.query(sess, [test_in, test_out])
        print("6")
        # real_query, real_mse = n.query(sess, [run_in, run_out])
        path = "D:\\github\\dinnersys_analysis\\machine_learning\\models\\{}_{}_{}_{}.ckpt".format(
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
            str(self.neuron_type),
            self.batch,
            self.step)
        # tf.train.Saver().save(sess, path)

        self.entity = {
            "show": {
                "path": path,
                "neuron_type": self.neuron_type,
                "batch": self.batch,
                "step": self.step,
                "learning_rate": self.learning_rate,
                "momentum": self.momentum,
                "real_accuracy": loss,
                "test_accuracy": test_mse,
                "loss": loss,
                "test_size": test_in.shape[0]
            },
            "data": {
                # "real_query": real_query,
                "test_input": test_in,
                "test_output": test_out,
                "test_query": test_query,
            }
        }
        gc.collect()


# -------------------------------------------------------------------------------------------------------------------- #
gene_bank = [
    genetic({
        "learning_rate": 1e-5,
        "momentum": 0.9,
        "algorithm": tf.train.MomentumOptimizer,
        "neuron_type": [],
        "batch": 5,
        "step": 10
    }),
]
'''
    genetic({
        "learning_rate": 1e-5,
        "momentum": 0.9,
        "algorithm": tf.train.MomentumOptimizer,
        "neuron_type": [400],
        "batch": 1000,
        "step": 10000
    }), genetic({
        "learning_rate": 1e-5,
        "momentum": 0.9,
        "algorithm": tf.train.MomentumOptimizer,
        "neuron_type": [400, 100],
        "batch": 1000,
        "step": 10000
    }), genetic({
        "learning_rate": 1e-5,
        "momentum": 0.9,
        "algorithm": tf.train.MomentumOptimizer,
        "neuron_type": [400, 100, 25],
        "batch": 5000,
        "step": 10000
    }),
    genetic({
        "learning_rate": 1e-5,
        "momentum": 0.9,
        "algorithm": tf.train.MomentumOptimizer,
        "neuron_type": [300, 300, 300],
        "batch": 5000,
        "step": 10000
    })
'''

'''
df = data_fetcher('2018-11-01', '2019-01-01')
data = df.get_train()
accu = accuracy(data[0], data[1], [
    datetime.strptime('2018-12-24', "%Y-%m-%d").timestamp(),
    datetime.strptime('2018-11-24', "%Y-%m-%d").timestamp(),
    # datetime.strptime('2018-10-24', "%Y-%m-%d").timestamp()
])
print("Created training data.")
file = open('data.pickle', 'wb')
pickle.dump(accu, file)

'''
pickle_in = open("data.pickle", "rb")
accu = pickle.load(pickle_in)

for g in gene_bank:
    tfconfig = tf.ConfigProto(device_count={'GPU': 0})
    with tf.Session(config=tfconfig) as sess:
        g.grow(accu, sess)
    tf.reset_default_graph()

for g in gene_bank:
    pprint.PrettyPrinter(4).pprint(g.entity["show"])

    if not g.rank():
        plt.figure(num='astronaut', figsize=(8, 8))
        plt.subplot(1, 2, 1)  # 将窗口分为两行两列四个子图，则可显示四幅图片
        plt.title("Query - {} - {}".format(g.entity["show"]["neuron_type"], g.entity["show"]["loss"]))  # 第一幅图片标题
        plt.imshow(g.entity["data"]["test_query"][0:1000].reshape(100, 10), plt.cm.gray)  # 绘制第一幅图片

        plt.subplot(1, 2, 2)
        plt.title('Origin')
        plt.imshow(g.entity["data"]["test_output"][0:1000].reshape(100, 10), plt.cm.gray)  # 绘制第二幅图片,且为灰度图
        plt.show()
