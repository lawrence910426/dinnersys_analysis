import numpy as np
import tensorflow as tf
import os

# import matplotlib as plt
# import os

BATCH_SIZE = 16

sizes = [3000, 5000, 1000]

input_x = tf.placeholder(dtype=tf.float32, shape=[None, 2])
target = tf.placeholder(dtype=tf.float32, shape=[None, 2])

global_step = tf.Variable(0, name="global_step", trainable=False)

x = tf.layers.dense(input_x, units=64, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=256, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=256, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=256, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=256, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=128, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=128, activation=tf.nn.leaky_relu)
x = tf.layers.dense(x, units=128, activation=tf.nn.leaky_relu)

output = tf.layers.dense(x, units=2)

loss = tf.reduce_mean(tf.squared_difference(target, output))

tf.summary.scalar("loss", loss)

merged = tf.summary.merge_all()
# minimize the loss

train_op = tf.train.AdamOptimizer(learning_rate=1e-3).minimize(loss, global_step=global_step)

'''

x = tf.Variable(tf.random_normal((1, sizes[0])))  # input layer
y = tf.Variable(tf.random_normal((1, sizes[2])))  # output layer

weight1 = tf.Variable(tf.random_normal((sizes[0], sizes[1])))
bias1 = tf.Variable(tf.random_normal((1, sizes[1])))
layer1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weight1), bias1))

weight2 = tf.Variable(tf.random_normal((sizes[1], sizes[2])))
bias2 = tf.Variable(tf.random_normal((1, sizes[2])))
layer2 = tf.nn.sigmoid(tf.add(tf.matmul(layer1, weight2), bias2))

cost = tf.nn.softmax_cross_entropy_with_logits_v2(layer2, y)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-3).minimize(cost)
'''
init = tf.global_variables_initializer()
train_writer = tf.summary.FileWriter(logdir="logs")
with tf.Session() as sess:
    sess.run(init)
    while True:
        input_x_train = np.random.rand(BATCH_SIZE, 2)
        target_train = np.cos(np.sin(input_x_train) ** 2)

        _, prediction, merged_summary_train, step = sess.run([train_op, output, merged, global_step], feed_dict={
            input_x: input_x_train,
            target: target_train
        })
        train_writer.add_summary(merged_summary_train, global_step=step)
        print("\r", step, end="")
        # print("prediction:", prediction, " real:", target_train)
