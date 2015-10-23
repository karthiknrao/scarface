import theano
import theano.tensor as T
import numpy as np

size = (4,5)
X = T.matrix()
Wx = theano.shared(
    np.ones(size),
    borrow=True
)
Wh = theano.shared(
    np.zeros((size[1],size[1])),
    borrow=True
)
b = theano.shared(
    np.zeros((size[1],)),
    borrow=True
)

"""
def step(x,h,Wx,Wh,b):
    o = T.nnet.sigmoid(T.dot(x,Wx)+T.dot(h,Wh) + b)
    return o
"""
def step(x,h):
    o = T.dot(x,Wx) + h
    return o

#func = theano.function( [X], o )
"""
X = T.matrix()
y0 = T.vector()
os,up = theano.scan(
    step,
    sequences=X,outputs_info=[y0],
    non_sequences=[Wx,Wh,b])
output = theano.function([X],os)

x = np.ones((10,4))
print output(x)

"""

X = T.scalar()
x = T.matrix()
h0 = T.vector()
os, up = theano.scan(
    step,
    sequences=x,
    outputs_info=[h0]
    )
func = theano.function([x,h0],os)
x = np.random.random((10,4))
hr = np.ones((5,))
print func(x,hr)
