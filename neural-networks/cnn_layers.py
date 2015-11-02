import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet.conv.conv2d
from theano.tensor.signal import downsample

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery):
        self.W = theano.shared(
            )
        self.b = theano.shared(
            )
        convout = conv2d(
            X,self.W,
            border_mode='valid',
        )
        self.params = [ self.W, self.b ]

    def __call__(self, X):
        act = lambda x : x if x >= 0 else 0
        return act( convout + self.b.dimshuffle('x',0,'x','x') )
        
class PoolLayer():
    def __init__(self,poolx,pooly,X):
        self.px = poolx
        self.py = pooly
    
    def __call__(self):
        return downsample.max_pool_2d(input,
                                      (px,py),
                                      ignore_border=True)
        
class FC():
    def __init__(self,insize,outsize,X):
        self.W = theano.shared(
            )
        self.b = theano.shared(
            )
        self.param = [ self.W, self.b ]
        
    def __call__(self):
        act = lambda x : x if x >= 0 else 0
        return act( T.dot(X,self.W) + self.b )

