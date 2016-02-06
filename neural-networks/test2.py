import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np
from layers import *
import cPickle, gzip, numpy

x = T.tensor4()

yinds = T.argsort(x,axis=3)
sliced = x
func = theano.function( [x], yinds )

X = np.random.random((2,2,3,4))

print X
print func(X)
