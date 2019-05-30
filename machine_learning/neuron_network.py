import tensorflow as tf
import matplotlib as plt
import os
import numpy as np
import math
import copy


class neuron_network:
    def __init__(self, input, hiddens, output, algorithm, batch):
        sizes = copy.deepcopy(hiddens)
        sizes.insert(0, len(input[0]))
        sizes.append(len(output[0]))

        self.BATCH_SIZE = batch

        self.input, self.output = input, output
        self.x = tf.Variable(np.zeros([self.BATCH_SIZE, self.input.shape[1]], dtype=np.float32), name='x',
                             trainable=False)  # training input layer
        self.y = tf.Variable(np.zeros([self.BATCH_SIZE, self.output.shape[1]], dtype=np.float32), name='y',
                             trainable=False)  # training output layer

        # self.x = tf.placeholder(tf.float32, [self.BATCH_SIZE, input.shape[1]], name='x')
        # self.y = tf.placeholder(tf.float32, [self.BATCH_SIZE, output.shape[1]], name='y')

        self.layers = []
        for i in range(len(sizes) - 1):
            prev_layer = self.x if i == 0 else self.layers[i - 1]["layer"]

            weight_value = tf.ones((sizes[i], sizes[i + 1])) / sizes[i] / sizes[i + 1]
            weight_value = weight_value if i % 2 == 0 else (0 - weight_value)
            weight = tf.Variable(weight_value)

            bias = tf.Variable(tf.zeros((1, sizes[i + 1])))
            if i == len(sizes) - 2:
                layer = tf.nn.sigmoid(tf.add(tf.matmul(prev_layer, weight), bias))
            else:
                layer = tf.nn.leaky_relu(tf.add(tf.matmul(prev_layer, weight), bias))
            self.layers.append({"layer": layer, "weight": weight, "bias": bias})

        self.result = self.layers[len(sizes) - 2]["layer"]
        self.cost = tf.losses.mean_squared_error(self.y, self.result)
        self.optimizer = algorithm.minimize(self.cost)

        self.debug = False

    def train(self, sess, steps):
        feed_in, feed_out = self.batch(sess, [self.input, self.output])
        init = tf.global_variables_initializer()
        sess.run(init)

        while True:
            try:
                sess.run(feed_in)
                sess.run(feed_out)
                for i in range(steps):
                    if i % 1 == 0 and self.debug:
                        self.show_debug(sess, i)
                    sess.run(self.optimizer)
            except tf.errors.OutOfRangeError:
                break

    def show_debug(self, sess, i):
        print(i, sess.run(self.cost))
        '''os.system("pause")
        for l in self.layers:
            print(sess.run(l["layer"]))
            print("weight", sess.run(l["weight"]))
            print("bias", sess.run(l["bias"]))
            print(sess.run(tf.gradients(self.cost, l["weight"])))
            print(sess.run(tf.gradients(self.cost, l["bias"])))
            print("-----")'''
        print("-------------------")
        print(sess.run(self.result))
        print(sess.run(self.y))
        print("--------------------------------------")

    def query(self, sess, data):
        result = np.zeros((data[0].shape[0], data[1].shape[1]))
        errors, ptr = 0, 0
        feed_input, feed_output = self.batch(sess, data)
        sse = tf.reduce_sum(tf.math.squared_difference(self.result, self.y))

        while True:
            try:
                sess.run(feed_input)
                sess.run(feed_output)
                tmp = sess.run(self.result)

                errors += sess.run(sse)
                end = min(ptr + self.BATCH_SIZE, data[0].shape[0])
                result[ptr:end] = tmp[0:end - ptr]
                ptr += self.BATCH_SIZE
            except tf.errors.OutOfRangeError:
                break
        return result, errors / (math.ceil(data[0].shape[0] / self.BATCH_SIZE) * self.BATCH_SIZE)

    def loss(self, sess):
        sum = 0
        feed_input, feed_output = self.batch(sess, [self.input, self.output])

        while True:
            try:
                sess.run(feed_input)
                sess.run(feed_output)
                sum += sess.run(self.cost) * self.BATCH_SIZE
            except tf.errors.OutOfRangeError:
                break
        return sum / self.input.shape[0]

    def batch(self, sess, arg):
        data = [None, None]
        data[0], data[1] = np.array(arg[0], dtype=np.float32), np.array(arg[1], dtype=np.float32)
        in_iterator = tf.data.Dataset.from_tensor_slices(data[0]).padded_batch(
            self.BATCH_SIZE, [data[0].shape[1], ]).make_initializable_iterator()
        out_iterator = tf.data.Dataset.from_tensor_slices(data[1]).padded_batch(
            self.BATCH_SIZE, [data[1].shape[1], ]).make_initializable_iterator()

        fuck_you_tf = tf.data.Dataset.from_tensor_slices(data[1]).padded_batch(
            self.BATCH_SIZE, [data[1].shape[1], ]).make_initializable_iterator()
        shit_you_tf = tf.data.Dataset.from_tensor_slices(data[1]).padded_batch(
            self.BATCH_SIZE, [data[1].shape[1], ]).make_initializable_iterator()

        sess.run(in_iterator.initializer)
        sess.run(out_iterator.initializer)
        sess.run(fuck_you_tf.initializer)
        sess.run(shit_you_tf.initializer)

        fuck_fuck_you_tf = fuck_you_tf.get_next()
        shit_shit_you_tf = shit_you_tf.get_next()
        padder_a = [[0, self.BATCH_SIZE - tf.shape(fuck_fuck_you_tf)[0]], [0, 0]]
        padder_b = [[0, self.BATCH_SIZE - tf.shape(shit_shit_you_tf)[0]], [0, 0]]

        self.get_next_in = tf.pad(in_iterator.get_next() , padder_a)
        self.get_next_out = tf.pad(out_iterator.get_next(), padder_b)

        feed_input = tf.assign(self.x, self.get_next_in)
        feed_output = tf.assign(self.y, self.get_next_out)
        return feed_input, feed_output
