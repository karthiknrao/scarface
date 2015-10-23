import theano
import theano.tensor as T
import numpy as np

class NARXLayer():
    def __init__(self,n_in,n_out):
        self.Wx = theano.shared(
            np.ones((n_in,n_out))
        )
        self.Wh = theano.shared(
            np.zeros((n_out,n_out))
        )
        self.b = theano.shared(
            np.zeros((n_out,))
        )

        self.Wo = theano.shared(
            np.zeros((n_out,))
        )
        self.bo = theano.shared(
            np.zeros((1,))
        )
        
        self.n_in = n_in
        self.n_out = n_out

    def params(self):
        return [ self.Wx,self.Wh,self.b ]
    
    def _step(self,x,h):
        o1 = T.dot(x,self.Wx) + T.dot(h,self.Wh) + self.b
        o2 = T.nnet.sigmoid(o1)
        o3 = T.dot(self.Wo,o2) + self.bo
        return T.nnet.sigmoid(o3)
        
    def output(self, X, y0):
        #y0 = np.zeros((1,self.n_out))
        y, up = theano.scan( 
            self._step,
            sequences=X,
            outputs_info=[y0],
        )
        return y


def loss_func( y_pred, y_true ):
    diff = (y_pred - y_true)**2
    return diff.sum(axis=-1).sum(axis=-1)

X = T.matrix()
y0 = T.vector()
yout = T.matrix()

rnnlayer1 = NARXLayer(4,5)
layer1o = rnnlayer1.output(X,y0)

"""
rnnlayer2 = RNNLayer((5,10))
layer2o = rnnlayer2.output(layer1o)
"""

params = rnnlayer1.params()
prediction = theano.function( [X,y0], layer1o )
cost = loss_func(layer1o,yout)
x = np.random.random((10,4))
y = np.ones((5,))
y_out = np.ones((10,5))
gradfunc = T.grad(cost,params[0])
#gfunc = theano.function([X,y0],gradfunc)
#print gfunc(x,y)
#gfunc = theano.function([X,y0,yout],gradfunc)
print prediction(x,y)
#print gfunc(x,y,y_out)
