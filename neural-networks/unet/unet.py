import theano
import theano.tensor as T
from theano.tensor.nnet import conv2d
from theano.tensor.signal import downsample
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from loaddata import *
import cv2

def relu(x):
    y = theano.tensor.switch(x<0, 0, x)
    return T.minimum(y, 2)

class ConvLayer():
    def __init__(self,insize,outsize,
                 filterx,filtery,mode='valid',act='relu'):
        self.W = theano.shared(
            np.asarray(
                np.random.randn(outsize,insize,filterx,filtery)*0.0001,
                dtype='float32'
            )
        )
        self.b = theano.shared(
            np.asarray(
                np.zeros((outsize)),
                dtype='float32'
            ) )
        self.mode = mode
        self.params = [ self.W, self.b ]
        self.act = act

    def __call__(self, X):
        act = relu
        if self.mode == 'same':
            convout = conv2d(
                X,self.W,
                border_mode='full',
            )[:,:,:-1,:-1]
        else:
            convout = conv2d(
                X,self.W,
                border_mode=self.mode,
            )
        if self.act == 'relu':
            return act( convout + self.b.dimshuffle('x',0,'x','x') )
        else:
            return convout + self.b.dimshuffle('x',0,'x','x') 

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
        self.params = []

    def __call__(self,X):
        output = T.repeat(X, self.xscale, axis=2)
        output = T.repeat(output, self.yscale, axis=3)
        return output

class Dropout():
    def __init__(self,level):
        self.level = level
        self.seed = 123
        self.params = []

    def __call__(self,X):
        rng = RandomStreams(seed=self.seed)
        retain_prob = 1. - self.level
        X *= rng.binomial(X.shape, p=retain_prob, dtype=x.dtype)
        X /= retain_prob
        return X

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
        ConvLayer(1024,512,2,2,'same',act=''),
        ConvLayer(1024,512,3,3),
        ConvLayer(512,512,3,3),
        UpSample(2,2),
        ConvLayer(512,256,2,2,'same',act=''),
        ConvLayer(512,256,3,3),
        ConvLayer(256,256,3,3),
        UpSample(2,2),
        ConvLayer(256,128,2,2,'same',act=''),
        ConvLayer(256,128,3,3),
        ConvLayer(128,128,3,3),
        UpSample(2,2),
        ConvLayer(128,64,2,2,'same',act=''),
        ConvLayer(128,64,3,3),
        ConvLayer(64,64,3,3),
        ConvLayer(64,2,1,1,act='')
]

params = []
for layer in enc + dec:
    params += layer.params

X = T.tensor4()
yt = T.ivector()
w = T.vector()

Xt = theano.shared(np.zeros((1,1,572,572),
                   dtype=theano.config.floatX),
                   borrow=True)
sharedy = theano.shared(np.zeros((388*388),
                   dtype=theano.config.floatX),
                   borrow=True)
Yt = T.cast(sharedy, 'int32')
Wt = theano.shared(np.zeros((388*388),
                   dtype=theano.config.floatX),
                   borrow=True)

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
decblock1conc = T.concatenate([encblock4[:,:,4:-4,4:-4],decblock1],axis=1)
decblock2 = dec[5](dec[4](dec[3](dec[2](decblock1conc))))
decblock2conc = T.concatenate([encblock3[:,:,16:-16,16:-16],decblock2],axis=1)
decblock3 = dec[9](dec[8](dec[7](dec[6](decblock2conc))))
decblock3conc = T.concatenate([encblock2[:,:,40:-40,40:-40],decblock3],axis=1)
decblock4 = dec[13](dec[12](dec[11](dec[10](decblock3conc))))
decblock4conc = T.concatenate([encblock1[:,:,88:-88,88:-88],decblock4],axis=1)
decblock5 = dec[16](dec[15](dec[14](decblock4conc)))

sftmxout = T.nnet.softmax(T.transpose(decblock5.reshape((2,388*388))))
output = T.argmax((T.transpose(sftmxout)).reshape((1,2,388,388)),axis=1)

def loss(yp,yt):
    return -T.mean(T.log(yp)[T.arange(yp.shape[0]), yt])

def loss2(yp):
    expr = yp
    return expr

cost2 = loss2(sftmxout)
cost = loss(sftmxout,yt)

grads = T.grad(cost,params)

def sgd_updates(grads,params,mom,lr):
    updates = []
    for grad,param in zip(grads,params):
        mparam = theano.shared(param.get_value()*0.)
        updates.append( (param,param - lr*mparam) )
        updates.append( (mparam,mparam*mom + (1.-mom)*grad) )
    return updates

#x = np.random.rand(1,1,572,572)

updates = sgd_updates(grads,params,0.99,0.0001)
train = theano.function( inputs=[],outputs=cost, updates=updates,
                         givens={ X : Xt, yt : Yt } )
costfunc = theano.function( inputs=[], outputs=cost, 
                            givens={X:Xt,yt:Yt} )
predict = theano.function( [X], sftmxout )

for image, label in readdataset('train','labels'):
    print image.shape, label.shape
    pimg = prepareinput(image).astype('float32')
    #output = predict(pimg)
    #pdb.set_trace()
    tlabels = np.array(label > 128, dtype='int')
    #ox = predict(pimg)
    #print ox.shape, ox
    #print output.shape, np.count_nonzero(output)
    print pimg.max()
    Xt.set_value(pimg)
    sharedy.set_value(tlabels.reshape(388*388).astype('float32'))
    Wt.set_value(np.ones((388*388)).astype('float32'))
    print costfunc()
    #print x.shape, x
    print 'Training'
    print train()

"""
out = predict(x)
print out.shape
print out
"""
