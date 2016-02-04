import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

def relu(x):
    return theano.tensor.switch(x<0, 0, x)

class CharEmbedding():
    def __init__(self,vecsize,vocabsize):
        valinit = np.zeros((vocabsize+1,vecsize))
        valinit[1:,:] = np.random.randn(vocabsize,vecsize)
        self.W = theano.shared(
            valinit
            )
        self.params = [ self.W ]
        
    def __call__(self,X):
        #out = self.W[:,X]
        def step(x):
            return self.W[:x]
        stk = theano.map( lambda x: self.W[x],X)
        out = T.stacklists(stk[0])
        #return out.dimshuffle('x','x',0,1)
        return out

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery):
        self.W = theano.shared(
            np.random.randn(outsize,insize,filterx,filtery)
            )
        self.b = theano.shared(
            np.random.randn(outsize)
            )
        self.params = [ self.W, self.b ]

    def __call__(self, X):
        act = T.nnet.sigmoid
        convout = conv2d(
            X,self.W,
            border_mode='full',
        )
        return act( convout + self.b.dimshuffle('x',0,'x','x') )

class PoolLayer():
    def __init__(self,poolx,pooly):
        self.px = poolx
        self.py = pooly
        self.params = []

    def __call__(self,X):
        return downsample.max_pool_2d(X,
                                      (self.px,self.py),
                                      ignore_border=True)

class FlattenLayer():
    def __init__(self):
        self.params = []

    def __call__(self,X):
        size = theano.tensor.prod(X.shape) // X.shape[0]
        nshape = (X.shape[0],size)
        return theano.tensor.reshape(X, nshape)

class FC():
    def __init__(self,insize,outsize):
        self.W = theano.shared(
            np.random.randn(insize,outsize)
            )
        self.b = theano.shared(
            np.random.randn(outsize)
            )
        self.params = [ self.W, self.b ]
        
    def __call__(self,X):
        act = T.nnet.sigmoid
        out = T.dot(X,self.W) + self.b
        return act( out )
