from rnn_layers import *
import theano
from theano.tensor as T

class LSTM():
    def __init__(self,n_in,n_out,X):
        self.nin = n_in
        self.nout = n_out
        self.inp = X
        self.lstm = rnn_layers.LSTM(self.nin,self.nout)
        self.lstmact = self.lstm.lstm_as_activation_function
        self.W = theano.shared(
            np.random.random(nout,nout)
            )
        self.b = theano.shared(
            np.random.random(nout)
            )
        self.h0 = theano.shared(
            np.zeros((nout,))
            )
        self.c0 = theano.shared(
            np.zeros((nout,))
            )
        
        self.params = lstm.params + [ self.W, self.b ]

    def output(self):
        
        def step(x,htm1,ctm1):
            h, c = self.lstmact(x,htm1,ctm1)
            y = T.dot(h,self.W) + self.b
            return h,c,y
        
        [h,c,y],_ = theano.scan(
            step,
            sequences=self.X,
            outputs_info=[self.h0,self.c0,None]
            )

        return y

def loss(y_pred, y):
    return -T.mean(T.log(y_pred)[T.arange(y.shape[0]), y])

L2_sqr = T.scalar()
y_true = T.ivector()
lr = T.scalar()
mom = T.scalar()

L2_sqr = 0
lstm_single = LSTM(26,26)
lstm_output = lstm_single.output()

yout = T.nnet.softmax(lstm_output)

for param in lstm_single.params:
    L2_sqr += (param**2).sum()

updates = {}
for param in lstm_single.params:
    updates[param] = theano.shared(
        value = np.zeros(
            param.get_value(
            borrow = True).shape,
            dtype = theano.config.floatX),
        name = 'updates')
        
cost = loss(yout,y_true) + L2_sqr

gparams = []
for param in lstm_single.params:
    gparams.append(T.grad(cost, param))

for param, gparam in zip(lstm_single.params, gparams):
    weight_update = self.updates[param]
    upd = mom * weight_update - lr * gparam
    updates[weight_update] = upd
    updates[param] = param + upd
