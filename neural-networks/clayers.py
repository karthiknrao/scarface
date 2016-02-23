import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

class TwoPathCNN():
    def __init__(self,k1,k2,ins,os1,maxout):
        self.Wk1 = theano.shared(
            np.random.randn(os1*maxout,ins,k1,k1)
        )
        
        
        self.Wk2 = theano.shared(
            np.random.randn(os1*maxout,os1,k2,k2)
        )
        """
        self.Wk3 = theano.shared(
            np.random.randn(os2,ins,k3,k3)
        )
        """
        self.maxout = maxout

    def __call__(self,X):
        convout = conv2d(
            X,self.Wk1,
            border_mode='valid',
        )
        
        maxout_out = None                                                       
        for i in xrange(self.maxout):                                            
            t = convout[:,i::self.maxout,:,:]                                   
            if maxout_out is None:                                              
                maxout_out = t                                                  
            else:                                                               
                maxout_out = T.maximum(maxout_out, t)

        convout2 = conv2d(
            maxout_out,self.Wk2,
            border_mode='valid',
        )
        
        maxout_out2 = None                                                       
        for i in xrange(self.maxout):                                            
            t = convout2[:,i::self.maxout,:,:]                                   
            if maxout_out2 is None:                                              
                maxout_out2 = t                                                  
            else:                                                               
                maxout_out2 = T.maximum(maxout_out2, t)

        return maxout_out2

x = T.tensor4()
twocnn = TwoPathCNN(7,3,4,10,2)
y = twocnn(x)

yout = theano.function( [x], y )
xin = np.random.rand(1,4,33,33)

o = yout(xin)
print o.shape
print o
