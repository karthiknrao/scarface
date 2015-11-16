import theano
import theano.tensor as T
import numpy as np
from dcnn_layers import *
import sys
import os
import re

def tokenize(x):
    clx = re.sub( "\.+|:+|\'+|\"", '', x )
    words = re.findall( '[a-z]+', clx )
    return words

tlines = [ x.strip().split(',') for x in open(sys.argv[1]).readlines() ]
datalabels = [ (x[-1].lower(),int(eval(x[0]))/2 ) for x in tlines ]
del tlines

words = []
for data, label in datalabels:
    words += tokenize(data)
    
words = dict([ (x,i+1) for i,x in enumerate(list(set(words))) ])

vocabs = len(words.keys())
print 'vocabs ', vocabs
layers = [ EmbeddingLayer(4,vocabs),
           ConvLayer(1,2,1,3),
           KMaxPoolLayer(5),
           ConvLayer(2,2,1,2),
           KMaxPoolLayer(3),
           FoldLayer(),
           FlattenLayer(),
           Dense(12,10),
           Dense(10,3) ]

params = []
x = T.ivector()
y = T.ivector()
lr = T.scalar()

o = layers[0](x)
params += layers[0].params
for i in range(1,len(layers)):
    params += layers[i].params
    o = layers[i](o)

neto = T.nnet.softmax(o)
yout = theano.function( [x], T.nnet.softmax(o) )

def loss(y_pred,y_true):
    return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

cost = loss(neto,y)
loss_func = theano.function([x,y],cost)
grads = T.grad(cost,params)

updates = [
    (param_i, param_i - 0.0001 * grad_i)
    for param_i, grad_i in zip(params, grads)
]

X = theano.shared( np.zeros((1000,31),dtype=np.int32) )
Y = theano.shared( np.zeros((1000, 1),dtype=np.int32) )
index = T.iscalar()
trainer = theano.function( [index], cost,
                           updates=updates,
                           givens={
                               x : X[index],
                               y : Y[index]
                               }
                       )

x = np.array( [ 10, 15, 1, 20 ], dtype=np.int32 )
y = np.array( [1], dtype=np.int32 )
#print yconv(x)
#print yout(x)
count = 0
b = 1000
buffx = np.zeros((1000,31),dtype=np.int32)
buffy = np.zeros((1000,1),dtype=np.int32)

for data,label in datalabels:
    tokens = tokenize(data)
    #print tokens
    ln = len(tokens)
    if ln > 30 or ln <= 3:
        continue
    for j in range(ln):
        buffx[count%b][j] = words[tokens[j]]
        buffx[count%b][-1] = ln
        buffy[count%b][0] = label
    if count % b == 0 and count > 0:
        X.set_value(buffx)
        Y.set_value(buffy)
        for k in range(1000):
            #print buffx[k][:buffx[k][-1]],buffx[k][-1]
            print trainer(k)
        buffx = np.zeros((1000,31),dtype=np.int32)
        buffy = np.zeros((1000,1),dtype=np.int32)

    count += 1
   

    
    """
    if len(tokens) < 3:
        continue
    wt = np.array([ words[t] for t in tokens ],dtype=np.int32 )
    yt = np.array( [ label ] , dtype=np.int32 )
    if count % 100 == 0:
        print trainer(wt,yt,0.0001)
    else:
        trainer(wt,yt,0.0001)
    count += 1
    """
