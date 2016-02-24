import theano
import theano.tensor as T
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal import downsample
import numpy as np
from clayers import *

fullPatch = T.tensor4()
centerPatch = T.tensor4()
ytruth = T.ivector()
index = T.iscalar()

fP = theano.shared(
    np.zeros((1000,4,65,65)),
    borrow=True
)
cP = theano.shared(
    np.zeros((1000,4,33,33)),
    borrow=True
)
yt = theano.shared(
    np.zeros((1000)),
    borrow=True
)
ylbls = T.cast(yt, 'int32')

stage1 = TwoPathCNN(4)
stage1out = stage1(fullPatch)
stage2 = TwoPathCNN(9)
stage2input = T.concatenate([stage1out,centerPatch],axis=1)
network_output = stage2(stage2input)

params = stage1.params + stage2.params

def nll(ypred,ytrue):
    shp = ypred.shape
    rypred = T.transpose(ypred.reshape((shp[1],shp[0]*shp[2]*shp[3])))
    return -T.mean(T.log(rypred)[T.arange(rypred.shape[0]),ytrue])

def errors(ypred,ytrue):
    shp = ypred.shape
    rypred = T.transpose(ypred.reshape((shp[1],shp[0]*shp[2]*shp[3])))
    preds = T.argmax(ryped,axis=1)
    return T.mean(T.neq(preds,ytrue))

l2norm = sum([ (x**2).sum() for x in params ])
l1norm = sum([ abs(x).sum() for x in params ])

cost = nll(network_output,ytruth) + l2norm + l1norm

grads = T.grad(cost,params)
    
def sgd_updates(grads,params,mom,lr):
    updates = {}
    for grad,param in zip(grads,params):
        mparam = theano.shared(param.get_value()*0.)
        updates[param] = param - lr*mparam
        updates[mparam] = mparam*mom + (1.-mom)*grad
    return updates

updates = sgd_updates(grads,params,0.9,0.001)

train_model = theano.function(
        inputs=[index],
        outputs=cost,
        updates=updates,
        givens={
            fullPatch: fP[index * 200: (index + 1) * 200],
            centerPatch : cP[index * 200: (index + 1) *200], 
            ytruth: ylbls[index * 200: (index + 1) * 200]
        }
    )
