import numpy as np
import theano
import theano.tensor as T

def single_layer_rnn(n_in,n_out):
    Wx = theano.shared(
        np.random.random((n_in,n_out))
    )
    Wh = theano.shared(
        np.random.random((n_out,n_out))
    )
    b = theano.shared(
        np.random.random((n_out,))
    )
    
    def step(x,htm1,Wx,Wh,b):
        h = T.dot(x,Wx) + T.dot(htm1,Wh) + b
        o = T.tanh(h)
        return h, o

    X = T.matrix()
    h0 = T.vector()
    yt = T.ivector()
    lr = T.scalar()

    [ h, y ], _ = theano.scan(step,
                              sequences=X,
                              outputs_info=[h0,None],
                              non_sequences=[Wx,Wh,b])
    yout = T.nnet.softmax(y)

    def loss(y_pred,y_true):
        return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

    oloss = loss(yout,yt)
    cost = theano.function( [X,h0,yt], oloss )
    funcy = theano.function( [X,h0], yout )
    funch = theano.function( [X,h0], h )
    [ gWx, gWh, gb ] = T.grad(oloss,[Wx,Wh,b])

    trainer = theano.function( [X,h0,yt,lr], 
                               oloss,
                               updates={
                                   Wx: Wx - lr * gWx,
                                   Wh: Wh - lr * gWh,
                                   b: b - lr * gb } )

    return [ funcy, funch, cost, trainer, [ Wx, Wh, b ] ]

srnn_y, srnn_h, cost, trainer, params = single_layer_rnn(26,26)

"""
def predict(X,hini):
    y = funcy(X,hini)
    return T.nnet.softmax(y)
"""
x = np.random.random((10,26))
y =  np.zeros((26,))
yt = np.array(range(10),dtype=np.int32)
print srnn_y(x , y)[0],srnn_h(x, y)[0]
print cost(x,y,yt)
for i in range(100000):
    loss = trainer(x,y,yt,100.0)
    #print loss
    if i % 1000 == 0:
        print i, loss
   

