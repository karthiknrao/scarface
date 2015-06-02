from skimage.feature import hog
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import glob, os, random, sys

def getBlocks(img,num):
    blocks = []
    if num == 5:
        blocks.append(img[0:200][0:200])
        blocks.append(img[0:200][50:250])
        blocks.append(img[50:250][0:200])
        blocks.append(img[50:250][50:250])
        blocks.append(img[25:225][25:225])
    elif num == 1:
        blocks.append(img[25:225][25:225])
    return blocks

dirs = glob.glob( sys.argv[1] + '/*' )
files = []
for dname in dirs:
    files += glob.glob( dname + '/*' )
    
outpath = 'hogdesc'
if not os.path.exists(outpath):
    os.mkdir(outpath)
    
posoutpath = 'hogdesc/pos'
if not os.path.exists(posoutpath):
    os.mkdir(posoutpath)

for i, fname in enumerate(files):
    img = rgb2gray( imread( fname ) )
    iblocks = getBlocks(img,1)
    for j, block in enumerate(iblocks):
        hogDesc = hog( block, orientations=9, \
                   pixels_per_cell=(8, 8),\
                   cells_per_block=(2, 2) )
        ofname = str(i) + '_' + str(j)
        outFile = os.path.join(posoutpath,ofname)
        np.save(outFile, hogDesc)
    print 'Done ..', fname
