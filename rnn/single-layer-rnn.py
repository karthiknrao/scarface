import numpy as np
import theano
import theano.tensor as T

# data http://www.gutenberg.org/ebooks/1661.txt.utf-8

def single_layer_rnn(n_in,n_out):
    Wx = theano.shared(
        np.random.randn(n_in,2*n_out)
    )
    Wh = theano.shared(
        np.random.randn(2*n_out,2*n_out)
    )
    b = theano.shared(
        np.random.randn(2*n_out,)
    )
    Wo = theano.shared(
        np.random.randn(2*n_out,n_out)
    )
    bo = theano.shared(
        np.random.randn(n_out,)
    )
    params = [ Wx, Wh, b, Wo, bo ]
    
    def step(x,htm1,Wx,Wh,b,Wo,bo):
        h = T.dot(x,Wx) + T.dot(htm1,Wh) + b
        o = T.nnet.sigmoid(h)
        y = T.nnet.sigmoid(T.dot(o,Wo) + bo)
        return o, y

    X = T.matrix()
    h0 = T.vector()
    yt = T.ivector()
    lr = T.scalar()
    mom = T.scalar()
    
    [ h, y ], _ = theano.scan(step,
                              sequences=X,
                              outputs_info=[h0,None],
                              non_sequences=[Wx,Wh,b,Wo,bo])
    yout = T.nnet.softmax(y)

    L2 = 0.001*((Wx**2).sum() + (Wh**2).sum() + (b**2).sum() +\
               (Wo**2).sum() + (bo**2).sum())
    
    def loss(y_pred,y_true):
        return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

    oloss = loss(yout,yt) + L2
    cost = theano.function( [X,h0,yt], oloss )
    funcy = theano.function( [X,h0], yout )
    funch = theano.function( [X,h0], h )
    #[ gWx, gWh, gb, gWo, gbo ] = T.grad(oloss,[Wx,Wh,b,Wo,bo])

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
                                                                                                        
    
    trainer = theano.function( [X,h0,yt,lr,mom], 
                               [oloss],
                               updates=updates )

    return [ funcy, funch, cost, trainer, [ Wx, Wh, b ] ]

#srnn_y, srnn_h, cost, trainer, params = single_layer_rnn(26,26)

"""
def predict(X,hini):
    y = funcy(X,hini)
    return T.nnet.softmax(y)
"""
"""
x = np.random.random((10,26))
y =  np.zeros((26,))
yt = np.array(range(10),dtype=np.int32)
"""
dataset = open('pg1661.txt').read().lower()[10000:11000]
#dataset = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + ' !"#$%&\'()*+,-./0123456789:;<=>?@')*1000
letters = list(set(dataset))

#data = (open('pg1661.txt').read()).lower()
data = dataset
srnn_y, srnn_h, cost, trainer, params = single_layer_rnn(len(letters),len(letters))

y =  np.zeros((2*len(letters),))
lrx = 0.0001
while True:
    for i in range(len(data)-20):
        xt = data[i:i+20]
        #yt = data[i+1:i+21]
        #print xt
        X = np.zeros((20,len(letters)))
        for j,x in enumerate(xt):
            X[j][letters.index(x)] = 1
        yt = np.array([ letters.index(x) for x in data[i+1:i+21] ], dtype=np.int32)
        loss = trainer(X,y,yt,0.00001,0.99)
        lrx = lrx - 0.000001
        if i % 1000 == 0:
            print loss
            out = srnn_y(X,y)
            outl = [ letters[np.argmax(x)] for x in out ]
            print list(xt),outl
    #y = srnn_h(X,y)[0]
    #print loss
    #print cost(X,y,yt)
    #if i % 100 == 0:
    #    print srnn_h(X,y)
    #print params
    """
    if i % 1000 ==  0:
        for f in range(20):
            print srnn_y(X,y)[f]
    """
    """
    print '#############################'
    for f in range(20):
        print srnn_y(X,y)[f]
    """
    
                 
"""
print srnn_y(x , y)[0],srnn_h(x, y)[0]
print cost(x,y,yt)
for i in range(100000):
    loss = trainer(x,y,yt,100.0)
    #print loss
    if i % 1000 == 0:
        print i, loss
   
"""
