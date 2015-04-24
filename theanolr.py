import os
import sys
import time
import numpy as np
import theano
import theano.tensor as T

w_init = np.random.rand(size)
w = theano.shared(
    value=w_init,
    name='w',
    borrow=True
    )
b_init = np.random.random()
b = theano.shared(
    value=b_init,
    name='b',
    borrow=True
    )

y = T.scalar( 'y' )
x = T.vector( 'x' )
rate = 0.1
lr = 0.01

yr = T.dot(w,x) + b
cost = ( y - yr )**2 + rate*T.sum(w**2)
costgrad = T.grad( cost, w )
updates = [ ( w, w - lr*costgrad ) ]

trainer = theano.function(
    inputs[x,y],
    outputs=cost,
    updates=updates
    )

def gen_training_data():
    noise = np.random.multivariate_normal(0,1)
    beta = np.array( [ 1,2,3,-1,3 ] )
    x = 
