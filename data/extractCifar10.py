import cPickle
import numpy as np
import cv2
import os

count = 0

def unpickle(file):
    global count
    fo = open(file, 'rb')
    dic = cPickle.load(fo)
    fo.close()
    labels = dic['labels']
    imgs = dic['data']
    for lab, img in zip( labels, imgs ):
        if not os.path.exists( str(lab) ):
            os.mkdir( str(lab) )
        outdir = str(lab)
        image = processEachImage( img )
        outpath = outdir + '/' + str(count) + '.jpeg'
        cv2.imwrite( outpath, image )
        count += 1
                
def processEachImage( block ):
    r = block[:1024]
    g = block[1024:1024*2]
    b = block[1024*2:]
    image = np.zeros((32,32,3))
    image[:,:,0] = r.reshape((32,32))
    image[:,:,1] = g.reshape((32,32))
    image[:,:,2] = b.reshape((32,32))
    return image

unpickle( 'data_batch_1' )
unpickle( 'data_batch_2' )
unpickle( 'data_batch_3' )
unpickle( 'data_batch_4' )
unpickle( 'data_batch_5' )
