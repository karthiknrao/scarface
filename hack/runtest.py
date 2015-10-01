from __future__ import absolute_import
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils
from load_data import *
from six.moves import range
import scipy.io.wavfile as sp
import sys, os, glob
import numpy as np

data_size = 8000*10
reshape_size = (400,200)
labels = 4

files = glob.glob( '*.mp3' )
labelid = [ 'angry', 'happy', 'neutral', 'unhappy' ]

def convertmp3wav(fname):
    cmd = 'sox %s temp.wav'
    os.system( cmd % fname )
    return

def read_wav(fname):
    (leng,data) = sp.read(fname)
    parts = []
    timelen = int(len(data)/float(8000))
    if leng == 8000:
        for i in range(0,timelen,10):
            if len(data[i*8000:8000*(i+10)]) == 8000*10:
                parts.append(data[i*8000:8000*(i+10)] + np.random.normal(0,10,8000*10))
    return parts

def do_classify(clf,parts):
    partpred = []
    buff = np.zeros((len(parts),1,reshape_size[0],reshape_size[1]))
    for i,part in enumerate(parts):
        rpr = part.reshape(reshape_size)
        buff[i] = rpr/float(2**16)
    output = clf.predict(buff)
    plabels = []
    for x in output:
        plabels.append(labelid[np.argmax(x)])
    return plabels

def run_classifier(classifier,files):
    for fname in files:
        convertmp3wav(fname)
        data = read_wav('temp.wav')
        predictions = do_classify(classifier,data)
        
        print( fname, predictions)

print( 'Compiling Model ....' )
model = Sequential()
model.add(Convolution2D(10,1,100,1,border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,1)))

model.add(Convolution2D(20, 10, 50, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,1)))

model.add(Convolution2D(30, 20, 25, 1, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(poolsize=(2,1)))

model.add(Flatten())
model.add(Dense(13*200*30, 2048))
model.add(Activation('relu'))

model.add(Dense(2048, 1024))
model.add(Activation('relu'))

model.add(Dense(1024, labels))

model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-4, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

print( 'Loading Weights ....' )
model.load_weights(sys.argv[1])

print( 'Running Predictions ....' )
run_classifier(model,files)
