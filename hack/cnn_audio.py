from __future__ import absolute_import
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from load_data import *
from six.moves import range

data_size = 8000*30
reshape_size = (1000,240)

model = Sequential()

model.add(Convolution2D(5,1,13,1,border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(4,1)))

model.add(Convolution2D(5, 5, 5, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

model.add(Convolution2D(10, 5, 4, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

model.add(Convolution2D(10, 10, 3, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

model.add(Flatten())
model.add(Dense(8*240*10, 2048))
model.add(Activation('relu'))

model.add(Dense(2048, 512))
model.add(Activation('relu'))

model.add(Dense(512, 4))
model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

data_files = read_files()
(train,test) = create_train_test(data_files,0.1)

for batch in makeBatches(train,1000):
    (X,y) = read_batch(batch)
    Y = np_utils.to_categorical(y, 4)
    X = X.astype("float32")
    Y = Y.astype("float32")
    X = X/float(2**16)
    print( 'Training..' )
    model.fit(X,Y,batch_size=100,nb_epoch=1)
