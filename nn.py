import os
import sys
import time
import numpy as np
import theano
import theano.tensor as T

class HiddenLayer():
    def __init__( self, input, isize, osize ):
        w = np.random.rand(osize, isize)
        W = theano.shared(
            value=w,
            name='W',
            borrow=True
            )
        b = np.random.rand(osize)
        B = theano.shared(
            value=b,
            name='B',
            borrow=True
            )
        o = T.dot(W,input) + B
        self.W = W
        self.B = B
        self.osize = osize
        self.isize = isize
        self.output = T.nnet.sigmoid( o )
        self.params = [ self.W, self.B ]

class NN():
    def __init__( self, input, isize ):
        self.h1 = HiddenLayer(
            input=input,
            isize=isize,
            osize=20
            )
        self.h2 = HiddenLayer(
            input=self.h1.output,
            isize=self.h1.osize,
            osize=10
            )
        self.h3 = HiddenLayer(
            input=self.h2.output,
            isize=self.h2.osize,
            osize=5
            )

        self.output = self.h3.output
        self.params = self.h1.params + self.h2.params + self.h3.params
        
    def costfunc( self, y ):
        return T.sum( ( self.output - y  )** 2 ) +\
          0.01*( T.sum(self.h1.W**2) + T.sum(self.h2.W**2) + T.sum(self.h3.W**2) )

i = T.scalar( 'i' )
x = T.vector( 'x' )
y = T.vector( 'y' )
NNet = NN( x, 10 )
cost = NNet.costfunc(y)
grads = [ T.grad(cost, param) for param in NNet.params ]
updates = [ ( param , param - 0.01*gparam )
            for param, gparam in zip( NNet.params, grads ) ]
trainer = theano.function(
    inputs=[x,y],
    outputs=cost,
    updates=updates,
    )
costf = theano.function(
    inputs=[x,y],
    outputs=cost
    )
datax = np.random.rand(100,10)
datay = np.random.rand(100,5)

for i in range(100):
    xi = datax[i]
    yi = datay[i]
    print 
    costvalue = costf(xi, yi)
    print 'CostValue ...', costvalue
    trainer( xi, yi )
