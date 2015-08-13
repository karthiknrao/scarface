import sys
import glob
import os

def readFiles(path):
    fileslabeled = []
    files = glob.glob(os.path.join(path,'*'))
    for fname in files:
        lbl = fname.split('-')[2]
        fileslabeled.append((fname,lbl))
    return fileslabeled

def create_train_test(files,frac):
    spairs =  [ (x[0],y[0],0) for i,x in enumerate(files)\
                for y in files[i:] if x[1] == y[1] ]
    nspairs = [ (x[0],y[0],1) for i,x in enumerate(files)\
                for y in files[i:] if x[1] != y[1] ]

    totalset = spairs + nspairs[:len(spairs)]
    trsize = int(len(totalset)*(1-frac))
    return (totalset[:trsize],totalset[trsize:])

def readBatch(files):
    batchx = np.zeros((2*len(files),3,100,100))
    batchy = np.zeros((2*len(files)))
    for i in range(len(files)):
        img = cv2.imread(files[i][0])
        batchx[2*i][0] = img[:,:,0]
        batchx[2*i][1] = img[:,:,1]
        batchx[2*i][2] = img[:,:,2]
        img = cv2.imread(files[i][1])
        batchx[2*i+1][0] = img[:,:,0]
        batchx[2*i+1][1] = img[:,:,1]
        batchx[2*i+1][2] = img[:,:,2]
        batchy[2*i] = files[i][2]
        batchy[2*i+1] = files[i][2]
    return (batchx, batchy)
