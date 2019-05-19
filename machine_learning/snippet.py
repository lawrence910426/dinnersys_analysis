import tensorflow as tf
import matplotlib as plt
import os

sizes = [3000 ,5000 ,1000]

x = tf.Variable(tf.random_normal((1 ,sizes[0])))      # input layer
y = tf.Variable(tf.random_normal((1 ,sizes[2])))      # output layer

weight1 =   tf.Variable(tf.random_normal((sizes[0], sizes[1])))
bias1 =     tf.Variable(tf.random_normal((1 ,sizes[1])))
layer1 =    tf.nn.sigmoid(tf.add(tf.matmul(x ,weight1) ,bias1))

weight2 =   tf.Variable(tf.random_normal((sizes[1] ,sizes[2])))
bias2 =     tf.Variable(tf.random_normal((1 ,sizes[2])))
layer2 =    tf.nn.sigmoid(tf.add(tf.matmul(layer1 ,weight2) ,bias2))

cost = tf.nn.softmax_cross_entropy_with_logits_v2(layer2 ,y)
optimizer = tf.train.AdamOptimizer(learning_rate=16).minimize(cost)

init = tf.global_variables_initializer()

config = tf.ConfigProto(device_count = {'GPU': 0})
with tf.Session(config=config) as sess:
    sess.run(init)
    for i in range(100):
        sess.run(optimizer)
        print(sess.run(cost))
        