from cnn_layers import *
import theano
import theano.tensor as T

X = T.4tensor()

layers = [ ConvLayer(3,10,5,5),
           PoolLayer(2,2),
           FC(10,10) ]

layer1o = ConvLayer(X)
layer2o = PoolLayer(layer1o)
layer3o = FC(layer2o)

