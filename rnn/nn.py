import theano
import theano.tensor as T
import numpy as np

class NNLayer():
    def __init__(self,n_in,n_out):
        self.W = theano.shared(
            np.ones((n_in,n_out))
        )
        self.b = theano.shared(
            np.ones((n_out,))
        )
        
    def output(self, X):
        o = T.dot( X, self.W ) + self.b
        return T.nnet.sigmoid(o)
        
    def params(self):
        return [ self.W, self.b ]

def loss_func(y_true,y_pred):
    diff = ( y_true - y_pred )**2
    return diff.sum(axis=-1).sum(axis=-1)

X = T.matrix()
Y = T.matrix()
params = []
nnlayer1 = NNLayer(4,5)
params += nnlayer1.params()
layer1o = nnlayer1.output(X)
nnlayer2 = NNLayer(5,10)
params += nnlayer2.params()
layer2o = nnlayer2.output(layer1o)
"""
cost = loss_func(layer2o,Y)

grads = T.grad(cost,params)
"""
#grad_func = theano.function( [X,Y], grads )
prediction = theano.function( [X], layer2o )

x = np.random.random((10,4))
#y = np.ones((5,10))
print prediction(x)
#print grad_func(x,y)
