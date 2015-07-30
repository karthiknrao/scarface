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

faces = '/media/karthik/0ed39684-ffb3-432a-bd76-d1e04ccd8716/administrator/data/face_patches'
nfaces = '/media/karthik/0ed39684-ffb3-432a-bd76-d1e04ccd8716/administrator/data/random_patches'
files = load_face_patches(faces) + load_notface_patches(nfaces)
(train,test,labels,lblmap) = create_train_test(files)


model = Sequential()
model.add(Convolution2D(10, 3, 5, 5, border_mode='full'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Convolution2D(30, 10, 5, 5, border_mode='full'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Convolution2D(30, 30, 3, 3, border_mode='full'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,2)))

model.add(Flatten())
model.add(Dense(64*8*8, 512))
model.add(Activation('relu'))

model.add(Dense(512, len(labels)))
model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

for batch in makeBatches(train,5000):
    (X,y) = read_batch(batch,lblmap)
    Y = np_utils.to_categorical(y, len(labels))
    model.train(X,Y)
    (X_test,y_test) = read_batch(batch,lblmap)
    Y_test = np_utils.to_categorical(y_test, len(labels))
    model.test(X_test,Y_test)
    
