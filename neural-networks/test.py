import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np
from layers import *
import cPickle, gzip, numpy
import pdb

f = gzip.open('mnist.pkl.gz', 'rb')
train_set, valid_set, test_set = cPickle.load(f)
f.close()
#pdb.set_trace()
X_train = train_set[0].reshape((train_set[0].shape[0],1,28,28))
X_labels = numpy.array(train_set[1],dtype=numpy.int32)
X_test = test_set[0].reshape((test_set[0].shape[0],1,28,28))
X_test_labels = numpy.array(test_set[1],dtype=numpy.int32)

x = T.tensor4()
x_test = T.tensor4()
y_test = T.ivector()
ylabels = T.ivector()
index = T.iscalar()

Xt = theano.shared(numpy.asarray(X_train,
                        dtype=theano.config.floatX),
                        borrow=True)
shared_y = theano.shared(numpy.asarray(X_labels,
                        dtype=theano.config.floatX),
                         borrow=True)
Yt = T.cast(shared_y, 'int32')

netlayers = [ ConvLayer(1,8,5,5),
           PoolLayer(2,2),
           ConvLayer(8,16,3,3),
           PoolLayer(2,2),
           FlattenLayer(),
           FC(9*9*16,100),
           FC(100,10) 
       ]

params = []
y = netlayers[0](x)
params += netlayers[0].params
for layer in netlayers[1:]:
    params += layer.params
    y = layer(y)

netout = T.nnet.softmax(y)

def lossfunc(ynet,ytrue):
    return -T.mean(T.log(ynet)[T.arange(ynet.shape[0]), ytrue])
    #return -T.mean(T.log(ynet)) + T.mean(ytrue)

def errors(ynet,ytrue):
    preds = T.argmax(ynet,axis=1)
    return T.mean(T.neq(preds,ytrue))

cost = lossfunc(netout,ylabels)
errfunc = errors(netout,y_test)
grads = T.grad(cost=cost,wrt=params)
gray = T.grad(cost,params[0])
updates = [ ( param,param - 0.5*grad ) for param, grad in\
            zip(params,grads) ]

train_model = theano.function(
        inputs=[index],
        outputs=cost,
        updates=updates,
        givens={
            x: Xt[index * 200: (index + 1) * 200],
            ylabels: Yt[index * 200: (index + 1) * 200]
        }
    )

test_model = theano.function(
    [x,y_test],
    errfunc
    )

yout = theano.function( [x], netout )
grady = theano.function( [x,ylabels],gray )
print params,grads
print X_labels[0:10]
print grady(X_train[0:2],X_labels[0:2])
for j in range(30):
    print test_model(X_test,X_test_labels)
    for i in range(250):
        print i,train_model(i)
