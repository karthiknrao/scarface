import numpy as np
import theano
import theano.tensor as T
import os

class LSTM():
    def __init__(self,n_in,n_out):
        self.Wxb = theano.shared(
            #np.random.randn(n_in,n_out),
            np.random.uniform(
                size = (n_in, n_out),
                low = -.01, high = .01)
            )
        self.Whb = theano.shared(
            #np.random.randn(n_out,n_out),
            np.random.uniform(
                size = (n_out, n_out),
                low = -.01, high = .01)
            )
        self.bb = theano.shared(
            #np.random.randn(n_out)
            np.random.uniform(
                size = (n_out,),
                low = -.01, high = .01)
            )

        self.Wxi = theano.shared(
            #np.random.randn(n_in,n_out),
            np.random.uniform(
                size = (n_in, n_out),
                low = -.01, high = .01)
        )
        self.Whi = theano.shared(
            #np.random.randn(n_out,n_out),
            np.random.uniform(
                size = (n_out, n_out),
                low = -.01, high = .01)
        )
        self.bi = theano.shared(
            #np.random.randn(n_out)
            np.random.uniform(
                size = (n_out,),
                low = -.01, high = .01)
        )

        self.Wxf = theano.shared(
            #np.random.randn(n_in,n_out),
            np.random.uniform(
                size = (n_in, n_out),
                low = -.01, high = .01)
        )
        self.Whf = theano.shared(
            #np.random.randn(n_out,n_out),
            np.random.uniform(
                size = (n_out, n_out),
                low = -.01, high = .01)
        )
        self.bf = theano.shared(
            #np.random.randn(n_out)
            np.random.uniform(
                size = (n_out,),
                low = -.01, high = .01)
        )

        self.Wxo = theano.shared(
            #np.random.randn(n_in,n_out),
            np.random.uniform(
                size = (n_in, n_out),
                low = -.01, high = .01)
        )
        self.Who = theano.shared(
            #np.random.randn(n_out,n_out),
            np.random.uniform(
                size = (n_out, n_out),
                low = -.01, high = .01)
        )
        self.bo = theano.shared(
            #np.random.randn(n_out)
            np.random.uniform(
                size = (n_out,),
                low = -.01, high = .01)
        )

        self.Wo = theano.shared(
            #np.random.randn(n_out,n_out)
            np.random.uniform(
                size = (n_out, n_out),
                low = -.01, high = .01)
            )
        self.bout = theano.shared(
            #np.random.randn(n_out)
            np.random.uniform(
                size = (n_out,),
                low = -.01, high = .01)
            )
        self.h0 = theano.shared(np.zeros(n_out,))
        self.c0 = theano.shared(np.zeros(n_out,))

        
        self.params = [ self.Wxb, self.Whb, self.bb,
                        self.Wxi, self.Whi, self.bi,
                        self.Wxf, self.Whf, self.bf,
                        self.Wxo, self.Who, self.bo ]
        
        self.params_l2 = [  self.Wo, self.bout]
        #self.params = [ self.Wxb, self.Whb, self.bb ] + self.params_l2
        
    def step(self,x,htm1,ctm1):
        z = T.tanh(
            T.dot(x,self.Wxb) + T.dot(htm1,self.Whb) + self.bb
            )
        i = T.nnet.sigmoid(
            T.dot(x,self.Wxi) + T.dot(htm1,self.Whi) + self.bi
            )
        f = T.nnet.sigmoid(
            T.dot(x,self.Wxf) + T.dot(htm1,self.Whf) + self.bf
            )
        c = i*z + f*ctm1
        o = T.nnet.sigmoid(
            T.dot(x,self.Wxo) + T.dot(htm1,self.Who) + self.bo
            )
        h = o*T.tanh(c)
        y = T.tanh(T.dot(h,self.Wo) + self.bout)
        return [h, c, y]
    
    def __call__(self, X):
        [ h, c, y ], _ = theano.scan(self.step,
                            sequences=X,
                            outputs_info=[self.h0,self.c0,None],
                            )

        return y

if not os.path.exists( 'pg1661.txt' ):
    os.system( 'wget -O pg1661.txt http://www.gutenberg.org/ebooks/1661.txt.utf-8' )

dataset = open('pg1661.txt').read().lower()[10000:20000]
#dataset = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + ' !"#$%&\'()*+,-./0123456789:;<=>?@')*1000
letters = list(set(dataset))
size = len(letters)
    
X = T.matrix()
yt = T.ivector()
lr = T.scalar()
mom = T.scalar()

params = []
params2 = []
lstm1 = LSTM(size,256)
lstm2 = LSTM(256,size)

layer1o = lstm1(X)
layer2o = lstm2(layer1o)
params += lstm1.params
params += lstm2.params
params += lstm1.params_l2
params += lstm2.params_l2
yout = T.nnet.softmax(layer2o)
L2 = T.scalar()
L2 = 0
for param in params:
    L2 += (param**2).sum()

L2 = 0.001*L2

def loss(y_pred,y_true):
    return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

#oloss = loss(yout,yt)
#cost = theano.function( [X,h0,c0,yt], oloss )
#funch = theano.function( [X,h0,c0], c )
srnn_y = theano.function([X],layer2o)

oloss = loss(yout,yt) + L2
cost = loss(yout,yt)
gparams = []
for param in params:
    gparams.append(T.grad(oloss, param))

# zip just concatenate two lists
updates_t = {}
    
for param in params:
    updates_t[param] = theano.shared(
        value = np.zeros(
            param.get_value(
            borrow = True).shape,
            dtype = theano.config.floatX),
            name = 'updates')

updates = {}
for param, gparam in zip(params, gparams):
    #weight_update = updates_t[param]
    upd =  - lr * gparam#+ mom * weight_update# - 0.01*param# + 
    #updates[weight_update] = upd
    updates[param] = param + upd

    """
    for param, gparam in zip(params, gparams):
        #mparam = theano.shared(param.get_value()*0.)
        upd = -lr*gparam# + mom*mparam# - 0.01*param# + 
        #updates[mparam] = upd
        updates[param] = param + upd
    """
    """            
        weight_update = updates[param]
        upd = -lr * gparam - 0.01*param
        updates[weight_update] = upd
        updates[param] = param + upd
    """
    
#gWxo = T.grad(oloss,Wxo)
#fgradwxo = theano.function( [X,h0,c0,yt], gWxo )
trainer = theano.function( [X,yt,lr],
                            [cost],
                            updates=updates )
    

#data = (open('pg1661.txt').read()).lower()
data = dataset
#srnn_y,trainer = single_layer_lstm(len(letters),len(letters))

#y =  np.zeros((2*len(letters),))
h = np.zeros((len(letters),))
c = np.zeros((len(letters),))

lrx = 0.01
mm = 0.9
while True:
    for i in range(len(data)-20):
        xt = data[i:i+20]
        #yt = data[i+1:i+21]
        #print xt
        X = np.zeros((20,len(letters)))
        for j,x in enumerate(xt):
            X[j][letters.index(x)] = 1
        yt = np.array([ letters.index(x) for x in data[i+1:i+21] ], dtype=np.int32)
        loss = trainer(X,yt,lrx)
        if loss[0] < 2.5:
            lrx = 0.0001
        #lrx = lrx - 0.000001
        if i % 100 == 0:
            #lrx -= 0.00001
            #if mm < 0.98:
            #    mm += 0.001
            print loss
            out = srnn_y(X)
            outl = [ letters[np.argmax(x)] for x in out ]
            print '| ' +xt+' |\n' ,'| '+''.join(outl)+' |\n'
