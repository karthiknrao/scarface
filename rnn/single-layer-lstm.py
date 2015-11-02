import numpy as np
import theano
import theano.tensor as T

def single_layer_lstm(n_in,n_out):
    Wxb = theano.shared(
        np.random.randn(n_in,n_out),
    )
    Whb = theano.shared(
        np.random.randn(n_out,n_out),
    )
    bb = theano.shared(
        np.random.randn(n_out)
    )

    Wxi = theano.shared(
        np.random.randn(n_in,n_out),
        )
    Whi = theano.shared(
        np.random.randn(n_out,n_out),
        )
    bi = theano.shared(
        np.random.randn(n_out)
        )
    #ci = theano.shared(
    #    np.random.random((n_out,))
    #    )

    Wxf = theano.shared(
        np.random.randn(n_in,n_out),
        )
    Whf = theano.shared(
        np.random.randn(n_out,n_out),
        )
    bf = theano.shared(
        np.random.randn(n_out)
        )
    #cf = theano.shared(
    #    np.random.random((n_out,))
    #    )

    Wxo = theano.shared(
        np.random.randn(n_in,n_out),
        )
    Who = theano.shared(
        np.random.randn(n_out,n_out),
        )
    bo = theano.shared(
        np.random.randn(n_out)
        )

    #co = theano.shared(
    #    np.random.random((n_out,))
    #    )

    #c = theano.shared(
    #    np.random.random((n_out,))
    #    )

    Wo = theano.shared(
        np.random.randn(n_out,n_out)
        )
    bout = theano.shared(
        np.random.randn(n_out)
        )
    
    params = [ Wxb,Whb,bb,Wxi,Whi,bi,Wxf,Whf,bf,
               Wxo,Who,bo,Wo,bout]

    def step(x,htm1,ctm1,Wxb,Whb,bb,\
             Wxi,Whi,bi,\
             Wxf,Whf,bf,\
             Wxo,Who,bo,Wo,bout):
        z = T.tanh(
            T.dot(x,Wxb) + T.dot(htm1,Whb) + bb
            )
        i = T.nnet.sigmoid(
            T.dot(x,Wxi) + T.dot(htm1,Whi) + bi
            )
        f = T.nnet.sigmoid(
            T.dot(x,Wxf) + T.dot(htm1,Whf) + bf
            )
        c = i*z + f*ctm1
        o = T.nnet.sigmoid(
            T.dot(x,Wxo) + T.dot(htm1,Who) + bo
            )
        h = o*T.tanh(c)
        y = T.tanh(T.dot(h,Wo) + bout)
        return [h, c, y]
    
    X = T.matrix()
    h0 = T.vector()
    c0 = T.vector()
    yt = T.ivector()
    lr = T.scalar()
    mom = T.scalar()

    [ h, c, y ], _ = theano.scan(step,
                              sequences=X,
                                 outputs_info=[h0,c0,None],
                              non_sequences=[Wxb,Whb,bb,
                                            Wxi,Whi,bi,
                                            Wxf,Whf,bf,
                                            Wxo,Who,bo,Wo,bout ]
                                )

    yout = T.nnet.softmax(y)
    L2 = T.scalar()
    L2 = 0
    for param in params:
        L2 += (param**2).sum()

    L2 = 0.001*L2

    def loss(y_pred,y_true):
        return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

    #oloss = loss(yout,yt)
    #cost = theano.function( [X,h0,c0,yt], oloss )
    funch = theano.function( [X,h0,c0], c )
    funcy = theano.function([X,h0,c0],y)

    oloss = loss(yout,yt)# + L2

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
    
    
    #gWxo = T.grad(oloss,Wxo)
    #fgradwxo = theano.function( [X,h0,c0,yt], gWxo )
    trainer = theano.function( [X,h0,c0,yt,lr,mom],
                               [oloss],
                               updates=updates )
    return funcy,trainer
"""
funcy, fgradwxo = single_layer_lstm(5,10)
x = np.random.random((4,5))
h = np.random.random((10,))
c = np.random.random((10,))
yt = np.array(range(4),dtype=np.int32)
print funcy(x,h,c)
print fgradwxo(x,h,c,yt)
"""

dataset = open('pg1661.txt').read().lower()
#dataset = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + ' !"#$%&\'()*+,-./0123456789:;<=>?@')*1000
letters = list(set(dataset))

#data = (open('pg1661.txt').read()).lower()
data = dataset
srnn_y,trainer = single_layer_lstm(len(letters),len(letters))

#y =  np.zeros((2*len(letters),))
h = np.zeros((len(letters),))
c = np.zeros((len(letters),))

lrx = 0.001
while True:
    for i in range(len(data)-10):
        xt = data[i:i+10]
        #yt = data[i+1:i+21]
        #print xt
        X = np.zeros((10,len(letters)))
        for j,x in enumerate(xt):
            X[j][letters.index(x)] = 1
        yt = np.array([ letters.index(x) for x in data[i+1:i+11] ], dtype=np.int32)
        loss = trainer(X,h,c,yt,lrx,0.9)
        #if loss[0] < 4.1:
        #    lrx = 0.0001
        #lrx = lrx - 0.000001
        if i % 100 == 0:
            print loss
            out = srnn_y(X,h,c)
            outl = [ letters[np.argmax(x)] for x in out ]
            print list(xt),outl
