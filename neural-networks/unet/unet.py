import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np

def relu(x):
    return theano.tensor.switch(x<0, 0, x)

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery,mode='valid'):
        self.W = theano.shared(
            np.random.randn(outsize,insize,filterx,filtery)
            )
        self.b = theano.shared(
            np.random.randn(outsize)
            )
        self.mode = mode
        self.params = [ self.W, self.b ]

    def __call__(self, X):
        act = T.nnet.sigmoid
        if self.mode == 'same':
            convout = conv2d(
                X,self.W,
                border_mode=(1,1),
            )
        else:
            convout = conv2d(
                X,self.W,
                border_mode=self.mode,
            )
        return act( convout + self.b.dimshuffle('x',0,'x','x') )

class PoolLayer():
    def __init__(self,poolx,pooly):
        self.px = poolx
        self.py = pooly
        self.params = []

    def __call__(self,X):
        return downsample.max_pool_2d(X,
                                      (self.px,self.py),
                                      ignore_border=True)

class UpSample():
    def __init__(self,xscale,yscale):
        self.xscale = xscale
        self.yscale = yscale
        
    def __call__(self,X):
        output = T.repeat(X, xscale, axis=2)
        output = T.repeat(output, yscale, axis=3)
        return output

#----------------------------------------------------------------------#

enc = [ ConvLayer(1,64,3,3),
        ConvLayer(64,64,3,3),
        PoolLayer(2,2),
        ConvLayer(64,128,3,3),
        ConvLayer(128,128,3,3),
        PoolLayer(2,2),
        ConvLayer(128,256,3,3),
        ConvLayer(256,256,3,3),
        PoolLayer(2,2),
        ConvLayer(256,512,3,3),
        ConvLayer(512,512,3,3),
        PoolLayer(2,2),
        ConvLayer(512,1024,3,3),
        ConvLayer(1024,1024,3,3),
]

dec = [ UpSample(2,2),
        ConvLayer(1024,512,2,2,'same'),
        ConvLayer(1024,512,3,3),
        ConvLayer(512,512,3,3),
        UpSample(2,2),
        ConvLayer(512,256,2,2,'same'),
        ConvLayer(512,256,3,3),
        ConvLayer(256,256,3,3),
        UpSample(2,2),
        ConvLayer(256,128,2,2,'same'),
        ConvLayer(256,128,3,3),
        ConvLayer(128,128,3,3),
        UpSample(2,2),
        ConvLayer(128,64,2,2,'same'),
        ConvLayer(128,64,3,3),
        ConvLayer(64,64,3,3),
        ConvLayer(64,2,1,1)
]

X = T.tensor4()

encblock1 = enc[1](enc[0](X))
encblock1pool = enc[2](encblock1)
encblock2 = enc[4](enc[3](encblock1pool))
encblock2pool = enc[5](encblock2)
encblock3 = enc[7](enc[6](encblock2pool))
encblock3pool = enc[8](encblock3)
encblock4 = enc[10](enc[9](encblock3pool))
encblock4pool = enc[11](encblock4)
encblock5 = enc[13](enc[12](encblock4pool))

decblock1 = dec[1](dec[0](encblock5))
decblock1conc = T.concatenate(encblock4[:,:,4:-4,4:-4],decblock1)
decblock2 = dec[5](dec[4](dec[3](dec[2](decblock1conc))))
decblock2conc = T.concatenate(encblock3[:,:,16:-16,16:-16],decblock2)
decblock3 = dec[9](dec[8](dec[7](dec[6](decblock2conc))))
decblock3conc = T.concatenate(encblock2[:,:,40:-40,40:-40],decblock3)
decblock4 = dec[13](dec[12](dec[11](dec[10](decblock3conc))))
decblock4conc = T.concatenate(encblock1[:,:,88:-88,88:-88],decblock4)
decblock5 = dec[15](dec[14](decblock4conc))

output = theano.function( [X], decblock5 )
outputshape = (1,2,388,388)
