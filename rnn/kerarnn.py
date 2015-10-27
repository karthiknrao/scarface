from __future__ import absolute_import
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.initializations import normal, identity
from keras.layers.recurrent import SimpleRNN, LSTM
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils

letters = list(set((open('pg1661.txt').read())))
data = (open('pg1661.txt').read()).lower()


model = Sequential()
model.add(SimpleRNN(output_dim=len(letters),
init=lambda shape: normal(shape, scale=0.001),
inner_init=lambda shape: identity(shape, scale=1.0),
activation='sigmoid', input_dim=len(letters)))
model.add(Dense(output_dim=len(letters),input_dim=len(letters)))
model.add(Activation('sigmoid'))
model.add(Activation('softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

for i in range(len(data)-20):
    xt = data[i:i+20]
    X = np.zeros((1,20,len(letters)))
    for j,x in enumerate(xt):
        X[0][j][letters.index(x)] = 1
    yt = np.array([ letters.index(x) for x in data[i+1:i+21] ], dtype=np.int32)
    Y = np_utils.to_categorical(yt, len(letters))
    model.fit(X,Y)
