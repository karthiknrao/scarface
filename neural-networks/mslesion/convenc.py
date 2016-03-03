import theano
import theano.tensor as T
from theano.tensor.nnet.conv3d2d import conv3d
import numpy as np
import sys

# input : (batch, time, in channel, row, column)
# filters : (out channel,time,in channel, row, column)

def max_nonlin(x):
    return theano.tensor.switch(x<0, 0, x)

tensor5 = T.TensorType(broadcastable=(False,False,False,False,False),
                       dtype=theano.config.floatX)
x = tensor5()
ytrue = tensor5()

wenc = theano.shared( 
    np.asarray(
        np.random.randn(10,4,1,4,4),
        dtype=theano.config.floatX )
    )
benc = theano.shared( 
    np.asarray(
        np.zeros(10,),
        dtype=theano.config.floatX )
    )
wdec = theano.shared( 
    np.asarray(
        np.random.randn(1,4,10,4,4),
        dtype=theano.config.floatX )
    )
bdec = theano.shared( 
    np.asarray(
        np.zeros(1,),
        dtype=theano.config.floatX )
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
    x = T.sum((((ytrue - ypred)**2)*ytrue))/T.sum(ytrue)
    y = T.sum((((ytrue - ypred)**2)*(1-ytrue)))/T.sum(1-ytrue)
    return r*x + (1-r)*y

cost = loss(convdec,ytrue)
grads = T.grad(cost,params)

def sgd_updates(grads,params,mom,lr):
    updates = []
    for grad,param in zip(grads,params):
        mparam = theano.shared(param.get_value()*0.)
        updates.append( (param,param - lr*mparam) )
        updates.append( (mparam,mparam*mom + (1.-mom)*grad) )
    return updates

updates = sgd_updates(grads,params,0.9,0.001)

trainer = theano.function(
    inputs=[x,ytrue],
    outputs=cost,
    updates=updates
    )

y = theano.function( [x], convdec )

xin = np.random.randn(1,100,1,100,100)

out = y(xin)

print 'HIIII',out.shape
