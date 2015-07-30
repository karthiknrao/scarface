import sys
import cv2
import os
import glob
import random

def load_face_patches(dname):
    datafiles = []
    files = glob.glob(os.path.join(dname,'*'))
    for fname in files:
        label = os.path.basename(fname).split('.')[0].split('_')[-1]
        datafiles.append((fname,label))
    return datafiles

def load_notface_patches(dname):
    datafiles = []
    files = glob.glob(os.path.join(dname,'*'))
    for fname in files:
        datafiles.append((fname,'nf'))
    return datafiles

def create_train_test(files):
    random.shuffle(files)
    labels = []
    for f in files:
        labels.append(f[1])
    labels = list(set(labels))
    trainsize = int(len(files)*0.9)
    train = files[:trainsize]
    test = files[trainsize:]
    return ( train, test, labels,
             { x : i for i,x in enumerate(labels)  } )

def read_batch(files,lbl):
    batchx = np.zeros((len(files),3,100,100))
    batchy = np.zeros((len(files,1)))
    for i,f in enumerate(files):
        img = cv2.imread(f[0])
        batchx[i][0] = img[:,:,0]
        batchx[i][1] = img[:,:,1]
        batchx[i][2] = img[:,:,2]
        batchy[i][0] = lbl[f[1]]
    return (batchx,batchy)

def makeBatches(inpList,size):
    for i in range(0,len(inpList),size):
        yield inpList[i:i+size]
