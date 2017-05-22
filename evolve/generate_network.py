import tensorflow as tf
import random
import sys, os
import numpy as np
import math
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

def get_output_nodes(blist):
    node_outs = []
    for i in range(len(blist)):
        out = 0
        for node in blist[i:]:
            out += node[i]
        node_outs.append(out)
    return ( [ k for k, val in enumerate(node_outs) if val > 0 ], \
                 [ k for k, val in enumerate(node_outs) if val == 0 ] + [ len(blist) ] )

def get_isolated_nodes(no_out,no_in):
    outset = set(no_out)
    inset = set(no_in)
    return list(outset.intersection(inset))

def get_len(nodes):
    return int((nodes)*(nodes-1)/2)

def listify(genome):
    l = len(genome)
    nodes = int(( -1 + math.sqrt(1 + 8*l) )/2)
    blists = []
    nodelens = [ get_len(x) for x in range(1,nodes+2) ]
    for i,x in enumerate(nodelens[:-1]):
        blists.append(genome[nodelens[i]:nodelens[i+1]])
    return blists

def create_stage(genome,input):
    layers = {}
    valid_nodes, output_nodes = get_output_nodes(genome)
    directinput_nodes = [0] + [ i+1 for i,x in enumerate(genome) if sum(x) == 0 ]
    isolated_nodes = get_isolated_nodes(output_nodes,directinput_nodes)
    nodes = [ i for i in range(len(genome)+1) if i not in isolated_nodes ]
    print( 'Genome ', genome )
    print( 'DirectInput Nodes ', directinput_nodes )
    print( 'Output Nodes ', output_nodes )
    print( 'Isolated Nodes ', isolated_nodes )
    print( 'Valid Nodes ', nodes )
    for node in nodes:
        if node != 0:
            layersum = sum(genome[node-1])
            print( 'Node ', node, genome[node-1], layersum )
        if node == 0 or layersum == 0:
            print('Node s 0:', node )
            layers['node_' + str(node)] = tf.layers.conv2d(inputs=input,filters=32,kernel_size=[3,3],
                                                           padding='same',
                                                           activation=tf.nn.relu)
            print('Node : ', node )
        else:
            print('Node s 1:', node )
            edges = [ i for i in range(node) if genome[node-1][i] == 1 ]
            print( 'Edges : ', edges )
            incoming = tf.add_n([ layers['node_' + str(i)] for i in edges ])
            layers['node_' + str(node)] = tf.layers.conv2d(inputs=incoming,filters=32,kernel_size=[3,3],
                                                           padding='same',
                                                           activation=tf.nn.relu)
            print('Node : ', node )
    print(output_nodes,layers.keys(),genome)
    outgoing = tf.add_n([ layers['node_' + str(i)] for i in output_nodes if i not in isolated_nodes ])
    output = tf.layers.conv2d(inputs=outgoing,filters=32,kernel_size=[3,3],padding='same',activation=tf.nn.relu)
    outputpool =  tf.layers.max_pooling2d(inputs=output, pool_size=[2, 2], strides=2)
    layers['output'] = outputpool
    return layers
            
def create_network(stages,genome):

    x = tf.placeholder("float", [None, 784])
    y = tf.placeholder("float", [None, 10])
    input_layer = tf.reshape(x, [-1, 28, 28, 1])
    layers = {}
    for i, num_nodes in enumerate(stages):
        print( 'Stages Num Nodes ', num_nodes )
        if i == 0:
            gl = get_len(num_nodes)
            stagegenome = genome[:gl]
            listifiedgen = listify(stagegenome)
            layers['stage_' + str(i)] = create_stage(listifiedgen,input_layer)
        else:
            glstart = 0
            for j in range(i):
                glstart += get_len(stages[j])
            glend = get_len(stages[i])
            stagegenome = genome[glstart:glstart+glend]
            print( 'Stage ', num_nodes, stagegenome )
            listifiedgen = listify(stagegenome)
            layers['stage_' + str(i)] = create_stage(listifiedgen,layers['stage_'+str(i-1)]['output'])
    poolout = layers['stage_' + str(len(stages)-1)]['output']
    pool2_flat = tf.reshape(poolout, [-1, 3 * 3 * 32])
    dense = tf.layers.dense(inputs=pool2_flat, units=500, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=True)
    logit = tf.layers.dense(inputs=dropout, units=10)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logit, labels=y))
    learning_rate = 0.001
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    
    with tf.Session() as sess:
        sess.run(init)
        training_epochs = 1
        batch_size = 50
        display_step = 1
        for epoch in range(training_epochs):
            avg_cost = 0.
            print( 'Epoch ', epoch )
            total_batch = int(mnist.train.num_examples/batch_size)
            for i in range(total_batch):
                print( 'Batch ', i )
                batch_x, batch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                              y: batch_y})
                avg_cost += c / total_batch
            if epoch % display_step == 0:
                print("Epoch:", '%04d' % (epoch+1), "cost=", \
                          "{:.9f}".format(avg_cost))
        print("Optimization Finished!")
        correct_prediction = tf.equal(tf.argmax(logit, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))

stages = [4,5,6]
totallen = sum([ int(x*(x-1)/2) for x in stages ])
print( 'Total Len ', totallen )
genome = [ 1 if random.random() < 0.5 else 0 for i in range(totallen) ]

create_network(stages,genome)
