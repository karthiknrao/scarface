import theano
import theano.tensor as T
from lasagne.layers import Conv2DLayer, InputLayer
from lasagne.layers import ElemwiseSumLayer, batch_norm
import lasagne
import random
import numpy as np
import sys
import os

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

def create_stage(incoming,binary_list):

    output_nodes, no_outputs = get_output_nodes(binary_list)
    no_inputs = [ k for k, node in enumerate(binary_list) if sum(node) == 0 ]
    isolated_nodes = get_isolated_nodes(no_outputs,no_inputs)
    

    print( 'List :', binary_list )
    print( 'Output nodes :', output_nodes )
    print( 'Isolated_nodes :', isolated_nodes )
    print( 'No Output nodes :', no_outputs )
    print( 'No Input nodes :', no_inputs )

    layers = []
    testx = T.tensor4()
    if isinstance(incoming,type(testx)):
        x = InputLayer(shape=(None,1,32,32),input_var=incoming)
        layers.append( batch_norm(
                Conv2DLayer(x,num_filters=32,filter_size=(3,3),\
                                       pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )
    else:
        x = incoming
        layers.append( batch_norm(
                Conv2DLayer(incoming,num_filters=32,filter_size=(3,3),\
                                       pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )

    for i, layer in enumerate(binary_list):
        if i == 0:
            if layer[0] == 0:
                layers.append( batch_norm(
                        Conv2DLayer(x,num_filters=32,filter_size=(3,3),\
                                               pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )
            else:
                layers.append( batch_norm(
                        Conv2DLayer(layers[0],num_filters=32,filter_size=(3,3),\
                                               pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )
        else:
            if sum(layer) == 0:
                layers.append( batch_norm(
                        Conv2DLayer(x,num_filters=32,filter_size=(3,3),
                                    pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )
            else:
                in_edges = []
                for k, edge in enumerate(layer):
                    if edge == 1:
                        in_edges.append(layers[k])
                o = ElemwiseSumLayer(in_edges)
                layers.append( batch_norm(
                        Conv2DLayer(o,num_filters=32,filter_size=(3,3),\
                                        pad='same',nonlinearity=lasagne.nonlinearities.rectify)) )
    
    outputs = [ layers[i] for i in output_nodes ]
    o = ElemwiseSumLayer(outputs)
    o = batch_norm( Conv2DLayer(o,num_filters=32,filter_size=(3,3),\
                                    pad='same',nonlinearity=lasagne.nonlinearities.rectify ) )

    return o

def make_classification_network(genome,stages,fcstage,labels):
    outs = []
    start = 0
    for i, num_nodes in enumerate(stages):
        #binary_list = [ [ 1 if random.random() < 0.5 else 0 for i in range(node) ] for node in range(1,num_nodes) ]
        l = int(((num_nodes)*(num_nodes - 1))/2)
        stage_genome = genome[start:start+l]
        seq = [ sum(range(0,j)) for j in range(1,num_nodes+1) ]
        binary_list = [ stage_genome[seq[k]:seq[k+1]] for k,s in enumerate(seq[:-1]) ]
        print(binary_list, 'stage :', num_nodes)
        start += l
        if i == 0:
            X = T.tensor4()
            o = create_stage(X,binary_list)
            outs.append(o)
            print(outs)
        else:
            print(outs)
            o_inter = lasagne.layers.MaxPool2DLayer(outs[-1],pool_size=(2,2))
            o = create_stage(o_inter,binary_list)
            outs.append(o)
    flatout = lasagne.layers.FlattenLayer(outs[-1])
    denseout = lasagne.layers.DenseLayer(flatout,num_units=100,nonlinearity=lasagne.nonlinearities.rectify)
    denseout2 = lasagne.layers.DenseLayer(denseout,num_units=labels,nonlinearity=lasagne.nonlinearities.softmax)
    return denseout2, X

def get_trainer(individual):
    out, X = make_classification_network(individual,[4,5,6],1,10)
    ytrue = T.ivector()
    prediction = lasagne.layers.get_output(out)
    loss = lasagne.objectives.categorical_crossentropy(prediction, ytrue)
    loss = loss.mean()
    
    params = lasagne.layers.get_all_params(out, trainable=True)
    updates = lasagne.updates.nesterov_momentum(
            loss, params, learning_rate=0.01, momentum=0.9)

    test_prediction = lasagne.layers.get_output(out, deterministic=True)
    test_loss = lasagne.objectives.categorical_crossentropy(test_prediction,
                                                            ytrue)
    test_loss = test_loss.mean()
    test_acc = T.mean(T.eq(T.argmax(test_prediction, axis=1), ytrue),
                      dtype=theano.config.floatX)
    train_fn = theano.function([X, ytrue], loss, updates=updates)
    val_fn = theano.function([X, ytrue], [test_loss, test_acc])

    return train_fn, val_fn

def evaluate(individual):
    train, test = get_trainer(individual)
    
    def load_dataset():
    
        if sys.version_info[0] == 2:
            from urllib import urlretrieve
        else:
            from urllib.request import urlretrieve

        def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
            print("Downloading %s" % filename)
            urlretrieve(source + filename, filename)

        import gzip

        def load_mnist_images(filename):
            if not os.path.exists(filename):
                download(filename)
        
            with gzip.open(filename, 'rb') as f:
                data = np.frombuffer(f.read(), np.uint8, offset=16)
            data = data.reshape(-1, 1, 28, 28)
            return data / np.float32(256)

        def load_mnist_labels(filename):
            if not os.path.exists(filename):
                download(filename)
        
            with gzip.open(filename, 'rb') as f:
                data = np.frombuffer(f.read(), np.uint8, offset=8)
        
            return data

    
        X_train = load_mnist_images('train-images-idx3-ubyte.gz')
        y_train = load_mnist_labels('train-labels-idx1-ubyte.gz')
        X_test = load_mnist_images('t10k-images-idx3-ubyte.gz')
        y_test = load_mnist_labels('t10k-labels-idx1-ubyte.gz')

        import cv2
        X_train_new = np.zeros((X_train.shape[0],1,32,32))
        X_test_new = np.zeros((X_train.shape[0],1,32,32))
        
        for i in range(X_train_new.shape[0]):
            X_train_new[i,0] = cv2.resize(X_train[i,0],(32,32))
        for i in range(X_test.shape[0]):
            X_test_new[i,0] = cv2.resize(X_test[i,0],(32,32))
    
        X_train_n, X_val_n = X_train_new[:-10000], X_train_new[-10000:]
        y_train_n, y_val_n = y_train[:-10000], y_train[-10000:]

        return X_train_new, y_train, X_test_new, y_test

    x_train,y_train,x_test,y_test = load_dataset()
    print(x_train.shape,y_train.shape)
    for epoch in range(2):
        print( 'Running epoch ', epoch )
        for batch in range(0,1000,100):
            train(x_train[batch:batch+100,:,:,:],y_train[batch:batch+100])
            print( 'Batch No ', batch )
    loss, acc = test(x_test[:1000,:,:,:],y_test[:1000])
    print(acc)
    return acc,

#binary_list = [ [ 1 if random.random() < 0.5 else 0 for i in range(node) ] for node in range(1,num_nodes) ]
L = sum([ int((x)*(x-1)/2) for x in [ 4,5,6 ] ])
print(L)
individual = [ 1 if random.random() < 0.5 else 0 for i in range(L) ]
print(individual)
result = evaluate(individual)
