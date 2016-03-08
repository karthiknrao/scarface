import theano
import theano.tensor as T
from theano.tensor.nnet.conv3d2d import conv3d
import numpy as np
import sys
from loaddata import *

# input : (batch, time, in channel, row, column)
# filters : (out channel,time,in channel, row, column)

path = '/media/karthik/My Passport/data/data/CHB_train_Case01'
#theano.config.floatX
def max_nonlin(x):
    return theano.tensor.switch(x<0, 0, x)

tensor5 = T.TensorType(broadcastable=(False,False,False,False,False),
                       dtype='float64')
x = tensor5()
ytrue = tensor5()

wenc = theano.shared( 
    np.asarray(
        np.random.randn(23,9,3,9,9),
        dtype='float64' )
    )
benc = theano.shared( 
    np.asarray(
        np.zeros(23,),
        dtype='float64' )
    )
wdec = theano.shared( 
    np.asarray(
        np.random.randn(1,9,23,9,9),
        dtype='float64' )
    )
bdec = theano.shared( 
    np.asarray(
        np.zeros(1,),
        dtype='float64' )
    )

params = [ wenc,benc,wdec,bdec ]
convenc = max_nonlin(
    conv3d(x,wenc) + benc.dimshuffle('x','x',0,'x','x')
    )
convdec = T.nnet.sigmoid(
    conv3d(convenc,wdec) + bdec.dimshuffle('x','x',0,'x','x')
    )

def loss(ypred,ytrue):
    r = 0.1
    x = T.sum((((ytrue - ypred)**2)*ytrue))/(1+T.sum(ytrue))
    y = T.sum((((ytrue - ypred)**2)*(1-ytrue)))/T.sum(1.0-ytrue)
    return r*x + (1-r)*y

cost = loss(convdec,ytrue)
grads = T.grad(cost,params)
gradwenc = T.grad(cost,wenc)

def sgd_updates(grads,params,mom,lr):
    updates = []
    for grad,param in zip(grads,params):
        mparam = theano.shared(param.get_value()*0.)
        updates.append( (param,param - lr*mparam) )
        updates.append( (mparam,mparam*mom + (1.-mom)*grad) )
    return updates

updates = sgd_updates(grads,params,0.9,1.0)

trainer = theano.function(
    inputs=[x,ytrue],
    outputs=cost,
    updates=updates
    )

test = theano.function( [x,ytrue],
                        T.sum(((ytrue-convdec)**2)*ytrue)/(1+T.sum(ytrue))
                        )

fgradwenc = theano.function( [x,ytrue],
                            gradwenc )
"""
y = theano.function( [x], convdec )

xin = np.random.randn(1,100,1,100,100)

out = y(xin)

print 'HIIII',out.shape
"""

#X,Y = readdata(path)
count = 0
for X,Y in readdata(path):
    print X.max()
    X = X/X.max()
    #X = X - X.mean()
    print X.max()
    print trainer(X,Y)
    print count
    count += 1
"""
Xs = tuple([1] + list(X.shape))
Ys = tuple([1] + list(Y.shape))
X = X.reshape(Xs)
Y = Y.reshape(Ys)
"""
"""
print X.shape,Y.shape
#print trainer(X,Y)
print fgradwenc(X,Y)
print test(X,Y)
"""
