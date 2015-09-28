import numpy as np
import glob
import os
import random

labels = [ 'angry', 'happy', 'neutral', 'unhappy' ]
#labels = [ 'neutral', 'happy']#, 'neutral', 'unhappy' ]
#random.seed(1234)

def read_files():
    files = []
    for i,dname in enumerate(labels):
        fs = glob.glob(os.path.join('data',dname,'*'))
        if dname == 'unhappy' and dname == 'angry':
            files += zip([1]*len(fs),fs)
        else:
            files += zip([0]*len(fs),fs)
        
        #files += zip([i]*len(fs),fs)
    return files

def create_train_test(files,part):
    random.shuffle(files)
    test = files[0:int(part*len(files))]
    train = files[int(part*len(files)):]
    return (train,test)

def makeBatches(inpList,size):
    for i in range(0,len(inpList),size):
        yield inpList[i:i+size]

def read_batch(files):
    batchx = np.zeros((len(files),1,400,200))
    batchy = np.zeros((len(files),1))
    for i,f in enumerate(files):
        img = np.load(f[1])
        batchx[i] = img.reshape((400,200))
        batchy[i] = int(f[0])
    return (batchx,batchy)
