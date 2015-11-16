import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery):
        self.W = theano.shared(
            np.random.random((outsize,insize,filterx,filtery))
            )
        self.b = theano.shared(
            np.random.random((outsize,))
            )
        self.params = [ self.W, self.b ]

    def __call__(self, X):
        act = T.tanh
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
                                      (px,py),
                                      ignore_border=True)
        
class KMaxPoolLayer():
    def __init__(self,kpool):
        self.poolsize = kpool
        self.params = []

    def __call__(self,X):
        ind = T.argsort(X, axis = 3)
        sorted_ind = T.sort(ind[:,:,:, -self.poolsize:], axis = 3)
        dim0, dim1, dim2, dim3 = sorted_ind.shape
        indices_dim0 = T.arange(dim0).repeat(dim1 * dim2 * dim3)
        indices_dim1 = T.arange(dim1).repeat(dim2 * dim3).reshape((dim1*dim2*dim3, 1)).repeat(dim0, axis=1).T.flatten()
        indices_dim2 = T.arange(dim2).repeat(dim3).reshape((dim2*dim3, 1)).repeat(dim0 * dim1, axis = 1).T.flatten()
        return X[indices_dim0, indices_dim1, indices_dim2, sorted_ind.flatten()].reshape(sorted_ind.shape)

class EmbeddingLayer():
    def __init__(self,vecsize,vocabsize):
        valinit = np.zeros((vecsize,vocabsize + 1))
        valinit[:,1:] = np.random.random((vecsize,vocabsize))
        self.W = theano.shared(
            valinit
            )
        self.params = [ self.W ]

    def __call__(self,X):
        n = X[30]
        out = self.W[:,X[:n]]
        return out.dimshuffle('x','x',0,1)

class FoldLayer():
    def __init__(self):
        self.params = []

    def __call__(self,X):
        return X[:,:,0::2,:] + X[:,:,1::2,:]
        
class FlattenLayer():
    def __init__(self):
        self.params = []

    def __call__(self,X):
        size = theano.tensor.prod(X.shape)
        return theano.tensor.reshape(X, (size,))

class Dense():
    def __init__(self,insize,outsize):
        self.W = theano.shared(
            np.random.random((insize,outsize))
            )
        self.b = theano.shared(
            np.random.random((outsize,))
            )
        self.params = [ self.W, self.b ]
        
    def __call__(self,X):
        act = T.tanh
        return act( T.dot(X,self.W) + self.b )
