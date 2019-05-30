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

'''
pickle_in = open("data.pickle", "rb")
accu = pickle.load(pickle_in)
'''

df = data_fetcher('2018-10-01', '2019-01-01')
data = df.get_train()
input = data[0]
output = data[1]
print("Created training data.")
accu = accuracy(input, output, [
    datetime.strptime('2018-12-24', "%Y-%m-%d").timestamp() ,
    datetime.strptime('2018-11-24', "%Y-%m-%d").timestamp() ,
    datetime.strptime('2018-10-24', "%Y-%m-%d").timestamp() ,
])
file = open('data.pickle', 'wb')
pickle.dump(accu, file)


print("Init tensorflow.")

tfconfig = tf.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.7))
# tfconfig = tf.ConfigProto(device_count = {'GPU': 0})

querys = []
neuron_types = [
    #[300, 100, 50],
    #[300, 150, 100],
    #[577, 223, 8],
    #[369, 123, 23],
    #[323, 221, 19],
    [400, 200, 50],
    #[200, 50, 10],
]
batches = [
    5000#, 10000, 20000
]

for batch in batches:
    for style in neuron_types:
        with tf.Session(config=tfconfig) as sess:
            test_in, test_out = accu.get_test()
            run_in, run_out = accu.get_run()
            n = neuron_network(
                run_in,
                style,
                run_out,
                tf.train.MomentumOptimizer(learning_rate=1e-4, momentum=0.9),
                batch
            )
            n.train(sess, 1000)
            test_query, test_mse = n.query(sess, [test_in, test_out])
            print("Queried for testing data")
            real_query, real_mse = n.query(sess, [run_in, run_out])
            print("Queried for running data")

            path = "D:\\github\\dinnersys_analysis\\machine_learning\\models\\{}_{}.ckpt".format(
                datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), str(style))
            querys.append({
                "path": path,
                "style": style,
                # "real_query": real_query,
                "real_accuracy": real_mse,

                "test_input": test_in,
                "test_output": test_out,
                "test_query": test_query,
                "test_accuracy": test_mse,
                "loss": n.loss(sess)
            })
            print("Queried for loss")

            tf.train.Saver().save(sess, path)
            print(style, path)
        tf.reset_default_graph()

for q in querys:
    print(q["style"], q["real_accuracy"], q["test_accuracy"], q["loss"], len(q["test_query"]))
    print(pd.DataFrame(q["test_query"][0:10]))
    print("------------------")
    print(pd.DataFrame(q["test_output"][0:10]))
    print("----------------------------------")

    mark = marker(q)
    if mark.is_trash():
        continue

    q["test_output"] = np.array(q["test_output"]) > 0.5
    q["test_query"] = np.array(q["test_query"])

    plt.figure(num='astronaut', figsize=(8, 8))
    plt.subplot(1, 2, 1)  # 将窗口分为两行两列四个子图，则可显示四幅图片
    plt.title("Query - {}".format(q["style"]))  # 第一幅图片标题
    plt.imshow(q["test_query"][0:1000].reshape(100, 10), plt.cm.gray)  # 绘制第一幅图片

    plt.subplot(1, 2, 2)
    plt.title('Origin')
    plt.imshow(q["test_output"][0:1000].reshape(100, 10), plt.cm.gray)  # 绘制第二幅图片,且为灰度图
    plt.show()
