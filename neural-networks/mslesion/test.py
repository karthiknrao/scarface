import theano
import theano.tensor as T
import numpy as np

x = T.tensor4()
y = T.tensor4()

def loss(ypred,ytrue):
    r = 0.1
    x = T.sum((((ytrue - ypred)**2)*ytrue))/T.sum(ytrue)
    y = T.sum((((ytrue - ypred)**2)*(1-ytrue)))/T.sum(1.0-ytrue)
    return r*x + (1-r)*y


cost = loss(x,y)

output = theano.function( [x,y], cost )

out = theano.function( [x], (x+x)**2*(x+2) )
X = np.random.binomial(1,0.1,(1,3,4,5))
Y = np.random.binomial(1,0.1,(1,3,4,5))
print out(X)
#print output(X,Y)
