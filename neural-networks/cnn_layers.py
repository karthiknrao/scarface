import numpy as np
import theano
import theano.tensor as T
import theano.tensor.nnet.conv.conv2d
from theano.tensor.signal import downsample

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery,X):
        self.W = theano.shared(
            )
        self.b = theano.shared(
            )
        convout = conv2d(
            X,self.W,
            border_mode='valid',
        )
        
        act = lambda x : x if x >= 0 else 0
        self.output = act( convout + self.b.dimshuffle('x',0,'x','x') )
        
class PoolLayer():
    def __init__(self,poolx,pooly,X):
        self.output = downsample.max_pool_2d(input,
                                             (poolx,pooly),
                                             ignore_border=True)
        
class FC():
    def __init__(self,insize,outsize,X):
        self.W = theano.shared(
            )
        self.b = theano.shared(
            )

        act = lambda x : x if x >= 0 else 0
        output = act( T.dot(X,self.W) + self.b )
