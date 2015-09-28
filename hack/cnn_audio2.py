from __future__ import absolute_import
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from load_data import *
from six.moves import range
#import pdb

data_size = 8000*10
reshape_size = (400,200)
labels = 2

model = Sequential()
model.add(Convolution2D(10,1,100,1,border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

model.add(Convolution2D(20, 10, 50, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

"""
model.add(Convolution2D(10, 5, 4, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))

model.add(Convolution2D(10, 10, 2, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(3,1)))
"""

model.add(Flatten())
model.add(Dense(17*200*20, 2048))
model.add(Activation('relu'))

"""
model.add(Dense(2048, 1024))
model.add(Activation('relu'))
"""
model.add(Dense(2048, labels))

model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

data_files = read_files()
print('No of Files', len(data_files))
(train,test) = create_train_test(data_files,0.1)

for i in range(10):
    count = 0

    for batch in makeBatches(train,1000):
        (X,y) = read_batch(batch)
        Y = np_utils.to_categorical(y, labels)
        X = X.astype("float32")
        Y = Y.astype("float32")
        X = X/float(2**16)
        #pdb.set_trace()
        print( 'Training..' )
        model.fit(X,Y,batch_size=100,nb_epoch=1)

        if count % 10 == 0:
            (X_test,y_test) = read_batch(test[:1000])
            Y_test = np_utils.to_categorical(y_test, labels)
            X_test = X_test.astype("float32")
            Y_test = Y_test.astype("float32")
            X_test = X_test/float(2**16)
            print( 'Eval...' )
            print(model.evaluate(X_test,Y_test,batch_size=100,show_accuracy=True))
            
            (X_test,y_test) = read_batch(test[1000:2000])
            Y_test = np_utils.to_categorical(y_test, labels)
            X_test = X_test.astype("float32")
            Y_test = Y_test.astype("float32")
            X_test = X_test/float(2**16)
            print( 'Eval...' )
            print(model.evaluate(X_test,Y_test,batch_size=30,show_accuracy=True))
        
        count += 1 
