import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

X = T.matrix()
yt = T.ivector()

x = T.nnet.softmax(X)
out = T.mean(T.log(x[T.arange(x.shape[0]), yt]))

func = theano.function( [X,yt], out )

x = np.random.randn(388*388,2).astype('float32')
y = np.array(np.random.rand(388*388) > 0.5,dtype='int').astype('int32')

print func(x,y)
