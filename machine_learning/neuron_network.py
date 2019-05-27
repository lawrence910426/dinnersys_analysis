import tensorflow as tf
import matplotlib as plt
import os
import numpy as np

class neuron_network:
    def __init__(self ,input ,hiddens ,output):
        sizes = hiddens
        sizes.insert(0 ,len(input[0]))
        sizes.append(len(output[0]))

        self.input ,self.output = input ,output
        self.x =        tf.Variable(np.array(input ,dtype=np.float32), name='x' ,trainable=False)           # training input layer
        self.y =        tf.Variable(np.array(output ,dtype=np.float32) ,name='y' ,trainable=False)          # training output layer

        self.layers = []
        for i in range(len(sizes) - 1):
            prev_layer =    self.x if i == 0 else self.layers[i - 1]["layer"]
            weight =        tf.Variable(tf.zeros((sizes[i], sizes[i + 1])))
            bias =          tf.Variable(tf.zeros((1 ,sizes[i + 1])))
            if i % 3 == 0 or i == len(sizes) - 2:
                layer =     tf.nn.sigmoid(tf.add(tf.matmul(prev_layer ,weight) ,bias))
            else:
                layer =     tf.nn.sigmoid(tf.add(tf.matmul(prev_layer ,weight) ,bias))
            self.layers.append({"layer" : layer ,"weight" : weight ,"bias" : bias})
        
        self.result = self.layers[len(sizes) - 2]["layer"]
        self.cost = tf.losses.softmax_cross_entropy(self.y ,self.result)
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(self.cost)

    def train(self ,sess ,steps):
        init = tf.global_variables_initializer()
        sess.run(init)
        for i in range(steps):
            if i % 100 == 0:
                print(i ,sess.run(self.cost))
                # os.system("pause")
                # for l in self.layers:
                #    print(sess.run(l["layer"]))
                # print(sess.run(self.result))
                # print(sess.run(self.y))
                # print("-------------------")
            sess.run(self.optimizer)

    def query(self ,sess ,data):
        result = []
        step = len(self.input)
        end = len(data)
        for i in range(0 , end, step):
            if i + step > end:
                tmp = data[i:end]
                while len(tmp) < step:
                    tmp.append([0 for j in range(len(self.input[0]))])
                tmp_result = sess.run(self.result ,feed_dict={'x:0' : tmp})
                for j in range(i ,end):
                    result.append(tmp_result[j - i])
            else:
                print(data[i:i+step])
                tmp_result = sess.run(self.result ,feed_dict={'x:0' : data[i:i+step]})
                for item in tmp_result:
                    result.append(item)
        return result
    
        
if __name__ == '__main__':
    n = neuron_network(
    [[10 ,3 ,3] ,[3 ,10 ,3]] ,
    [6 for i in range(0)], 
    [[1 if i % 3 == 0 else 0 for i in range(6)] ,[1 if i % 3 == 1 else 0 for i in range(6)] ])

    with tf.Session(config=tf.ConfigProto(device_count = {'GPU': 0})) as sess:
        n.train(sess ,1000)
        print(n.query(sess , [[10 ,3 ,3] ,
            [3 ,10 ,3]]))
