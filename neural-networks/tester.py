import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np
from layers import *
import cPickle, gzip, numpy
import pdb

x = T.matrix()
"""
layer1 = ConvLayer(1,2,3,3)
layer2 = PoolLayer(2,2)
layer3 = FlattenLayer()
"""
layer4 = FC(15*15*2,10)
#params = layer1.params + layer2.params + layer3.params + layer4.params
params = layer4.params 
#y = T.mean(layer4(layer3(layer2(layer1(x)))))
y = T.mean(layer4(x))
grady = T.grad(y,params[0])
func = theano.function([x],grady)
funcy = theano.function([x],y)
x = np.random.random((100,15*15*2))
print func(x)
print funcy(x)
