import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

class TwoPathCNN():
    def __init__(self):
        # filter widths
        # p1 = path1, p2 = path2
        self.p1_k1_width = 7
        self.p1_k2_width = 3
        self.p2_k1_width = 13
        self.final_width = 21

        # input and output channels
        self.maxout = 2
        self.inp_chn = 4
        self.p1_k1_ochn = 64
        self.p1_k2_ochn = 64
        self.p2_k1_ochn = 160
        self.final_ochn = 5

        self.Wp1_k1 = theano.shared(
            np.random.randn(self.p1_k1_ochn*self.maxout,
                            self.inp_chn,self.p1_k1_width,self.p1_k1_width)
        )
        self.bp1_k1 = theano.shared(
            np.random.randn(self.p1_k1_ochn*self.maxout)
        )

        self.Wp1_k2 = theano.shared(
            np.random.randn(self.p1_k2_ochn*self.maxout,
                            self.p1_k1_ochn,self.p1_k2_width,self.p1_k2_width)
        )
        self.bp1_k2 = theano.shared(
            np.random.randn(self.p1_k2_ochn*self.maxout)
        )

        self.Wp2_k1 = theano.shared(
            np.random.randn(self.p2_k1_ochn*self.maxout,
                            self.inp_chn,self.p2_k1_width,self.p2_k1_width)
        )
        self.bp2_k1 = theano.shared(
            np.random.randn(self.p2_k1_ochn*self.maxout)
        )

        self.Wfinal = theano.shared(
            np.random.randn(self.final_ochn,self.p2_k1_ochn + self.p1_k2_ochn,
                            self.final_width,self.final_width)
        )
        self.bfinal = theano.shared(
            np.random.randn(self.final_ochn)
        )

        self.params = [ self.Wp1_k1, self.Wp1_k2, self.Wp2_k1, self.Wfinal,
                        self.bp1_k1, self.bp1_k2, self.bp2_k1, self.bfinal ]

    def __call__(self,X):

        ## path1 with kernel widths 7 and 3
        convout = conv2d(
            X,self.Wp1_k1,
            border_mode='valid',
        ) + self.bp1_k1.dimshuffle('x',0,'x','x')
        pool_convout = downsample.max_pool_2d(convout, (4,4), 
                          ignore_border=None, st=(1,1), padding=(0, 0))

        maxout_out = None                                                       
        for i in xrange(self.maxout):                                            
            t = pool_convout[:,i::self.maxout,:,:]                                   
            if maxout_out is None:                                              
                maxout_out = t                                                  
            else:                                                               
                maxout_out = T.maximum(maxout_out, t)

        
        convout2 = conv2d(
            maxout_out,self.Wp1_k2,
            border_mode='valid',
        ) + self.bp1_k2.dimshuffle('x',0,'x','x')
        pool_convout2 = downsample.max_pool_2d(convout2, (2,2), 
                              ignore_border=None, st=(1,1), padding=(0, 0))
        

        maxout_out2 = None                                                       
        for i in xrange(self.maxout):                                            
            t = pool_convout2[:,i::self.maxout,:,:]                                   
            if maxout_out2 is None:                                              
                maxout_out2 = t                                                  
            else:                                                               
                maxout_out2 = T.maximum(maxout_out2, t)

        # end of path1

        # path2 with kernel width 13
        convout3 = conv2d(
            X,self.Wp2_k1,
            border_mode='valid',
        ) + self.bp2_k1.dimshuffle('x',0,'x','x')
        
        maxout_out3 = None                                                       
        for i in xrange(self.maxout):                                            
            t = convout3[:,i::self.maxout,:,:]                                   
            if maxout_out3 is None:                                              
                maxout_out3 = t                                                  
            else:                                                               
                maxout_out3 = T.maximum(maxout_out3, t)
        
        # end of path2

        # final convolution before output
        stacked_out = T.concatenate([maxout_out2,maxout_out3],axis=1)

        full_conv_out = conv2d(
            stacked_out,self.Wfinal,
            border_mode='valid',
        ) + self.bfinal.dimshuffle('x',0,'x','x')

        # output size (5x1x1)
        return full_conv_out



#testing
x = T.tensor4()
twocnn = TwoPathCNN()
y = twocnn(x)

yout = theano.function( [x], y )
xin = np.random.rand(1,4,33,33)

o = yout(xin)
print o.shape
#print o
