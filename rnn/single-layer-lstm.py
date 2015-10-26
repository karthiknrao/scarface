import numpy as np
import theano
import theano.tensor as T

def single_layer_lstm(n_in,n_out):
    Wxb = theano.shared(
        np.random.random((n_in,n_out)),
    )
    Whb = theano.shared(
        np.random.random((n_out,n_out)),
    )
    bb = theano.shared(
        np.random.random((n_out,))
    )

    Wxi = theano.shared(
        np.random.random((n_in,n_out)),
        )
    Whi = theano.shared(
        np.random.random((n_out,n_out)),
        )
    bi = theano.shared(
        np.random.random((n_out,))
        )
    ci = theano.shared(
        np.random.random((n_out,))
        )

    Wxf = theano.shared(
        np.random.random((n_in,n_out)),
        )
    Whf = theano.shared(
        np.random.random((n_out,n_out)),
        )
    bf = theano.shared(
        np.random.random((n_out,))
        )
    cf = theano.shared(
        np.random.random((n_out,))
        )

    Wxo = theano.shared(
        np.random.random((n_in,n_out)),
        )
    Who = theano.shared(
        np.random.random((n_out,n_out)),
        )
    bo = theano.shared(
        np.random.random((n_out,))
        )
    co = theano.shared(
        np.random.random((n_out,))
        )

    c = theano.shared(
        np.random.random((n_out,))
        )

    def step(x,htm1,c,Wxb,Whb,bb,\
             Wxi,Whi,bi,ci,\
             Wxf,Whf,bf,cf,\
             Wxo,Who,bo,co):
        z = T.tanh(
            T.dot(x,Wxb) + T.dot(htm1,Whb) + bb
            )
        i = T.tanh(
            T.dot(x,Wxi) + T.dot(htm1,Whi) + ci*c + bi
            )
        f = T.tanh(
            T.dot(x,Wxf) + T.dot(htm1,Whf) + cf*c + bf
            )
        c = i*z + f*c
        o = T.tanh(
            T.dot(x,Wxo) + T.dot(htm1,Who) + co*c + bo
            )
        y = o*T.tanh(c)
        return y, c
    
    X = T.matrix()
    h0 = T.vector()
    c0 = T.vector()
    yt = T.ivector()
    
    [ y, c ], _ = theano.scan(step,
                              sequences=X,
                              outputs_info=[h0,c0],
                              non_sequences=[Wxb,Whb,bb,
                                            Wxi,Whi,bi,ci,
                                            Wxf,Whf,bf,cf,
                                            Wxo,Who,bo,co ]
                                )

    yout = T.nnet.softmax(y)

    def loss(y_pred,y_true):
        return -T.mean(T.log(y_pred)[T.arange(y_true.shape[0]), y_true])

    oloss = loss(yout,yt)
    cost = theano.function( [X,h0,c0,yt], oloss )
    funch = theano.function( [X,h0,c0], c )
    funcy = theano.function([X,h0,c0],y)

    gWxo = T.grad(oloss,Wxo)
    fgradwxo = theano.function( [X,h0,c0,yt], gWxo )
    return funcy, fgradwxo

funcy, fgradwxo = single_layer_lstm(5,10)
x = np.random.random((4,5))
h = np.random.random((10,))
c = np.random.random((10,))
yt = np.array(range(4),dtype=np.int32)
print funcy(x,h,c)
print fgradwxo(x,h,c,yt)
