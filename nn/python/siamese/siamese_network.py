from __future__ import absolute_import
from __future__ import print_function
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from six.moves import range
from load_dataset import *

path = '/home/indix/karthik/scarface/nn/python/datarot'
files = readFiles(path)
(train,test) = create_train_test(files,0.1)

model = Sequential()
model.add(Convolution2D(10, 3, 5, 5, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Convolution2D(30, 10, 5, 5, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Convolution2D(30, 30, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Flatten())
model.add(Dense(3000, 512))
model.add(Activation('relu'))

model.add(Dense(512, 50))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='siamese_euclidean', optimizer=sgd)

def do_siamese_predict(model,X,Y):
    y_pred = model.predict(X,batch_size=100)
    left = y_pred[0::2]
    right = y_pred[1::2]
    dist = ( left - right )**2
    pred = []
    for i in range(len(Y)):
        pred.append( 1 if dist[i] > 0.5 else 0 )
    return np.array(pred)

for batch in makeBatches(train,1000):
    (X,y) = read_batch(batch)
    Y = y
    X = X.astype("float32")
    Y = Y.astype("float32")
    X = X/255.0
    X = X - meanimg
    print( 'Training..' )
    model.fit(X,Y,batch_size=100,nb_epoch=1)

    (X_test,y_test) = read_batch(test)
    Y_test = np_utils.to_categorical(y_test, len(labels))
    X_test = X_test.astype("float32")
    Y_test = Y_test.astype("float32")
    X_test = X_test/255.0
    X_test = X_test - meanimg
    print( 'Eval...' )
    #model.evaluate(X_test,Y_test,batch_size=100,show_accuracy=True)
    print(do_siamese_predict(model,X_test,Y_test))
