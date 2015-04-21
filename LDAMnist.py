import idx2numpy
import numpy as np
from sklearn.lda import LDA
from multiprocessing import Pool
import pdb

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

#numbers = [ (x, y) for x in range(10) for y in range(x,10) if x != y ]

def runTestPairs( e ):
    x = e[0]; y = e[1]
    trainX = labelsmaptra[x] + labelsmaptra[y]
    labelsX = [x]*len(labelsmaptra[x]) + [y]*len(labelsmaptra[y])

    clf = LDA()
    clf.fit( trainX, labelsX )

    testX = labelsmaptes[x] + labelsmaptes[y]
    labelsX = [x]*len(labelsmaptes[x]) + [y]*len(labelsmaptes[y])
    error = 0
    for lab, test in zip( labelsX, testX ):
        pred = clf.predict(test)
        if lab != pred:
            error += 1
    print e, error, error/float(len(testX))
    return ( e, error, error/float(len(testX)) )

def runTestMultiClass( e ):
    x = e[0]; y = e[1]; z = e[2]
    trainX = labelsmaptra[x] + labelsmaptra[y] + labelsmaptra[z]
    labelsX = [x]*len(labelsmaptra[x]) + [y]*len(labelsmaptra[y]) +\
        [z]*len(labelsmaptra[z])

    clf = LDA()
    clf.fit( trainX, labelsX )

    testX = labelsmaptes[x] + labelsmaptes[y] + labelsmaptes[z]
    labelsX = [x]*len(labelsmaptes[x]) + [y]*len(labelsmaptes[y]) +\
        [z]*len(labelsmaptes[z])
        
    error = 0
    for lab, test in zip( labelsX, testX ):
        pred = clf.predict(test)
        if lab != pred:
            error += 1
    print e, error, error/float(len(testX))
    return ( e, error, error/float(len(testX)) )

numbers = [ (x, y, z) for x in range(10) for y in range(x,10) for z in range(y,10) if x != y != z ]
#pool = Pool( processes=2 )
#results = pool.map( runTestMultiClass, numbers )

onestwos = np.array(labelsmaptra[1][0:500] + labelsmaptra[2][0:500])
U,D,V = np.linalg.svd(onestwos)
pdb.set_trace()
