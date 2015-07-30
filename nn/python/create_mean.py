import sys
import os
import numpy as np
import cv2
import glob

def makeBatches(inpList,size):
    for i in range(0,len(inpList),size):
        yield inpList[i:i+size]

w = int(sys.argv[2])
h = w
bsize = 5000

files = []
files += glob.glob(os.path.join(sys.argv[1],'*'))
files += glob.glob(os.path.join(sys.argv[2],'*'))

mean_file = np.zeros((h,w,3),dtype='float32')
batchimg = np.zeros((bsize,h,w,3),dtype='float32')
count = 0
for batch in makeBatches(files,bsize):
    for i,imagefile in enumerate(batch):
        batchimg[i] = cv2.imread(imagefile)
    size = len(batch)
    batchimg = batchimg[:size]/255.0
    batchmean = batchimg.mean(0)
    mean_file = ((count/(count+size+0.0))*mean_file + (1/(count+size+0.0))*batchmean)
    count += size

