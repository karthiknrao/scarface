import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

class TwoPathCNN():
    def __init__(self,inpsize):
        # filter widths
        # p1 = path1, p2 = path2
        self.p1_k1_width = 7
        self.p1_k2_width = 3
        self.p2_k1_width = 13
        self.final_width = 21

        # input and output channels
        self.maxout = 2
        self.inp_chn = inpsize
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

        # softmax
        shp = full_conv_out.shape
        resized = T.transpose(full_conv_out.reshape((shp[1],shp[0]*shp[2]*shp[3])))
        output = T.nnet.softmax(resized)
        
        return T.transpose(output).reshape(shp)


"""
by stacking two instances of this module
we can create model variation 1 in the paper
Fig 3(a)
"""

"""
TBD : Loss function, optimizer
"""

# how to create network in fig 3(a)

fullPatch = T.tensor4()
centerPatch = T.tensor4()

stage1 = TwoPathCNN(4)
stage1out = stage1(fullPatch)
stage2 = TwoPathCNN(9)
stage2input = T.concatenate([stage1out,centerPatch],axis=1)
stage2out = stage2(stage2input)

network_output = theano.function([fullPatch,centerPatch],stage2out)

fpatch = np.random.randn(1,4,65,65)
cpatch = fpatch[:,:,16:16+33,16:16+33]

output = network_output(fpatch,cpatch)
print output.shape
print output
