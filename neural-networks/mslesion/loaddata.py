import SimpleITK
import sys
import cv2
import os
import numpy as np

filetypes = [ '_FLAIR', '_T1', '_T2', '_lesion' ]

def readdata(path):
    files = [ os.path.join( path, os.path.basename( path ) + x + '.nhdr' )
              for x in filetypes ]
    data = [ SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(x))\
             for x in files[:-1] ]
    labels = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(files[-1]))
    dataset = np.zeros((1,512,3,512,512))
    for i in range(512):
        for j in range(3):
            dataset[0,i,j,:,:] = data[j][i]
    labelsp = labels.reshape((1,512,1,512,512))
    size = 100
    for i in range(0,512,100):
        for j in range(0,512,100):
            for k in range(0,512,100):
                yield dataset[:,i:i+size,:,j:j+size,k:k+size],labelsp[:,i+8:i+size-8,:,j+8:j+size-8,k+8:k+size-8]
