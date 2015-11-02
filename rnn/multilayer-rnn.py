import numpy as np
import theano
import theano.tensor as T

class RNN():
    def __init__(self,n_in,n_out):
        self.Wx = theano.shared(
            np.random.randn(n_in,2*n_out)
        )
        self.Wh = theano.shared(
            np.random.randn(2*n_out,2*n_out)
        )
        self.b = theano.shared(
            np.random.randn(2*n_out,)
        )
        self.Wo = theano.shared(
            np.random.randn(2*n_out,n_out)
        )
        self.bo = theano.shared(
            np.random.randn(n_out,)
        )

        #self.X = T.matrix()
        #self.h0 = T.vector()

    def step(self,x,htm1):
        h = T.dot(x,self.Wx) + T.dot(htm1,self.Wh) + self.b
        o = T.nnet.sigmoid(h)
        y = T.nnet.sigmoid(T.dot(o,self.Wo) + self.bo)
        return o, y

    def params(self):
        return [ self.Wx, self.Wh, self.b, self.Wo, self.bo ]
    
    def output(self,X,h0):
        [ h, y ], _ = theano.scan(self.step,
                              sequences=X,
                              outputs_info=[h0,None])
        return y

X = T.matrix()
h0 = T.vector()
h1 = T.vector()
params = []

dataset = open('pg1661.txt').read().lower()[10000:11000]
dataset = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + ' !"#$%&\'()*+,-./0123456789:;<=>?@')*1000
letters = list(set(dataset))
insize = len(letters)

rnnlayer1 = RNN(insize,100)
params += rnnlayer1.params()
outlayer1 = rnnlayer1.output(X,h0)
rnnlayer2 = RNN(100,insize)
params += rnnlayer2.params()
outlayer2 = rnnlayer2.output(outlayer1,h1)

yt = T.ivector()
lr = T.scalar()
mom = T.scalar()
L2 = T.scalar()
L2 = 0

yout = T.nnet.softmax(outlayer2)
 
for param in params:
    L2 += (param**2).sum()

L2 += 0.001*L2

def loss(y_pred,y_true):
        return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

oloss = loss(yout,yt) + L2
cost = theano.function( [X,h0,h1,yt], oloss )
funcy = theano.function( [X,h0,h1], yout )
#funch = theano.function( [X], h )

gparams = []
for param in params:
    gparams.append(T.grad(oloss, param))

# zip just concatenate two lists
updates = {}

for param in params:
    updates[param] = theano.shared(
    value = np.zeros(
        param.get_value(
        borrow = True).shape,
        dtype = theano.config.floatX),
        name = 'updates')
    
for param, gparam in zip(params, gparams):
    weight_update = updates[param]
    upd = mom * weight_update - lr * gparam
    updates[weight_update] = upd
    updates[param] = param + upd
    
trainer = theano.function( [X,h0,h1,yt,lr,mom], 
                               [oloss],
                               updates=updates )

#data = (open('pg1661.txt').read()).lower()
data = dataset
y0 = np.zeros((2*len(letters),))
y1 = np.zeros((2*100,))
lrx = 0.0001
segs = 5
while True:
    for i in range(len(data)-segs):
        xt = data[i:i+segs]
        #yt = data[i+1:i+21]
        #print xt
        X = np.zeros((segs,len(letters)))
        for j,x in enumerate(xt):
            X[j][letters.index(x)] = 1
        yt = np.array([ letters.index(x) for x in data[i+1:i+segs+1] ], dtype=np.int32)
        loss = trainer(X,y1,y0,yt,0.00001,0.99)
        #print loss
        lrx = lrx - 0.000001
  
        if i % 1000 == 0:
            print loss
            out = funcy(X,y1,y0)
            outl = [ letters[np.argmax(x)] for x in out ]
            print list(xt),outl
       
