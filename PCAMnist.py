import idx2numpy
import numpy as np
from sklearn.lda import LDA
from multiprocessing import Pool
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import pdb
import cv2

imagestra = idx2numpy.convert_from_file('train-images.idx3-ubyte')
labelstra = idx2numpy.convert_from_file('train-labels.idx1-ubyte')

labelsmaptra = { x : [] for x in list( set( list(labelstra))) }
imagesArray = []
for i in range(len(imagestra)):
    imagesArray.append( imagestra[i].reshape( (1, (28*28)))[0] )

for lab, img in zip( list(labelstra), imagesArray ):
    labelsmaptra[lab].append( img )

imagestes = idx2numpy.convert_from_file('t10k-images.idx3-ubyte')
labelstes = idx2numpy.convert_from_file('t10k-labels.idx1-ubyte')

labelsmaptes = { x : [] for x in list( set( list(labelstes))) }
imagesArray = []
for i in range(len(imagestes)):
    imagesArray.append( imagestes[i].reshape( (1, (28*28)))[0] )

for lab, img, in zip( list(labelstes), imagesArray ):
    labelsmaptes[lab].append( img )

def getError(model, vec):
    cvals = model.transform(vec)
    cvalst = np.transpose(cvals)
    values = cvalst * model.components_
    pred = np.sum(values, axis=0 )
    return ((pred - vec )*(pred - vec)).sum()
    
"""
for key in labelsmaptra.keys():
    outdir = str(key)
    if not os.path.exists( outdir ):
        os.mkdir( str(key) )
    for i, img in enumerate(labelsmaptra[key]):
        cv2.imwrite( outdir + '/' + str(i) + '.jpeg', img.reshape((28,28)) )
""" 


"""
for i in range(20):
    plt.imshow( pca.components_[i].reshape( (28,28) ) )
    plt.savefig( str(i) + '.jpeg' )
"""

models = []
for i in range(10):
    models.append( PCA( n_components=5 ) )
    
for i in range(10):
    print 'Training For ..', i
    models[i].fit(labelsmaptra[i])

print 'Starting test ..'
error = 0
total = 0
for key in labelsmaptes.keys():
    total += len(labelsmaptes[key])
    print 'Testing ..', key
    for x in labelsmaptes[key]:
        scores = []
        for i, model in enumerate(models):
            scores.append(getError(model, x ))
        scores = np.array(scores)
        args = np.argsort(scores)
        pred = args[0]
        if pred != key:
            #print pred, key, scores
            error += 1
            
print 'Error Rate ..', error/float(total)
"""
print 'Errors ', 5
for x in labelsmaptes[5][:100]:
    print getError(pca, x )

print 'Errors ', 9
for x in labelsmaptes[8][:10]:
    print getError(pca, x )
"""
