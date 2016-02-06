import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np
from layers import *
import cPickle, gzip, numpy
import pdb

x = T.matrix()
yt = T.ivector()
y = T.argmax(x,axis=1)
maxx = theano.function([x],y)
errors = T.mean(T.neq(y,yt))
err = theano.function([y,yt],errors)
xx = np.array( [ [1,2,3,4],[5,1,2,4] ] )
y = np.array( [1,2], dtype=np.int32 )
print maxx(xx)
o = maxx(xx)
print err(o,y)
