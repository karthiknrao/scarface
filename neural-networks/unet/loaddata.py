import cv2
import os
import math
import numpy as np

def readdataset(train,test,augment=True):
    trainfiles = [ os.path.join(train,'frame%d.tif' % i)\
                   for i in range(30) ]
    testfiles = [ os.path.join(test,'frame%d.tif' % i)\
                  for i in range(30) ]

    for tr,ts in zip(trainfiles,testfiles):
        imgtr = cv2.imread(tr,0)
        imgts = cv2.imread(ts,0)
        #yield imgtr, imgts
        for angle in range(1,91,1):
            cos = math.cos(math.radians(angle))
            sin = math.sin(math.radians(angle))
            size = int(512*(cos+sin))
            sl = (size - 512)/2
            print angle,size,sl
            imgr = cv2.resize(imgtr,(size,size))
            rows, cols = imgr.shape
            M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
            rotr = cv2.warpAffine(imgr,M,(cols,rows))[sl:sl+512,sl:sl+512]
            
            imgr = cv2.resize(imgts,(size,size))
            rows, cols = imgr.shape
            M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
            rots = cv2.warpAffine(imgr,M,(cols,rows))[sl:sl+512,sl:sl+512]

            yield rotr, rots[62:-62,62:-62]
            yield cv2.flip(rotr,1), cv2.flip(rots,1)[62:-62,62:-62]
            yield cv2.flip(rotr,0), cv2.flip(rots,0)[62:-62,62:-62]
            yield cv2.flip(cv2.flip(rotr,1),0), cv2.flip(cv2.flip(rots,1),0)[62:-62,62:-62]
            
    #for tr, ts in zip(trainfiles,testfiles):
        
def prepareinput(img):
    fullimg = np.zeros((572,572))
    fullimg[30:-30,30:-30] = img
    fullimg[0:30,30:-30] = cv2.flip(img[0:30,:],0)#top
    fullimg[30:-30,0:30] = cv2.flip(img[:,0:30],1)#left
    fullimg[30:-30,-30:] = cv2.flip(img[:,-30:],1)#right
    fullimg[-30:,30:-30] = cv2.flip(img[-30:,:],0)#bottom
    fullimg[0:30,0:30] = cv2.flip(img[0:30,0:30],-1)#tlcorner
    fullimg[0:30,-30:] = cv2.flip(img[0:30,-30:],-1)#trcorner
    fullimg[-30:,0:30] = cv2.flip(img[-30:,0:30],-1)#blcorner
    fullimg[-30:,-30:] = cv2.flip(img[-30:,-30],-1)#brcorner
    norm = np.array(fullimg,dtype='float')/255.0
    norm = (norm - norm.mean())
    return norm.reshape((1,1,572,572))
