from skimage.feature import hog
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import glob, os, random, sys
from bs4 import BeautifulSoup

def getBlocks(img,num):
    blocks = []
    if num == 5:
        blocks.append(img[0:200,0:200])
        blocks.append(img[0:200,50:250])
        blocks.append(img[50:250,0:200])
        blocks.append(img[50:250,50:250])
        blocks.append(img[25:225,25:225])
    elif num == 1:
        blocks.append(img[25:225,25:225])
    return blocks

def getRndBlocks(img):
    blocks = []
    if img.shape[0] <= 200 or img.shape[1] <= 200:
        return blocks
    xy = [ ( int(random.random()*(img.shape[0]-200)),\
             int(random.random()*(img.shape[1]-200)) ) \
             for i in range(5) ]
    for x,y in xy:
        #print x, y, img.shape,img[x:x+200,y:y+200].shape
        blocks.append(img[x:x+200,y:y+200])
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
    #iblocks = []
    for j, block in enumerate(iblocks):
        ofname = str(i) + '_' + str(j)
        outFile = os.path.join(posoutpath,ofname)
        #if os.path.exists(outFile + '.npy'):
        #    continue
        hogDesc = hog( block, orientations=9, \
                   pixels_per_cell=(8, 8),\
                   cells_per_block=(2, 2) )
        np.save(outFile, hogDesc)
    print 'Done ..', fname

negoutpath = 'hogdesc/neg'
if not os.path.exists(negoutpath):
    os.mkdir(posoutpath)

annotatepath = '/home/karthik/data/VOCdevkit/VOC2012/Annotations/*'
imgpath = '/home/karthik/data/VOCdevkit/VOC2012/JPEGImages/'

vocfiles = glob.glob( annotatepath )

def parse(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    names = [ x.text.encode('ascii', 'ignore') for x in soup.findAll( 'name' ) ]
    return [ x.lower() for x in names ]

npfiles = []
for fname in vocfiles:
    tags = parse(fname)
    if 'person' not in tags:
        imagename = fname.split('/')[-1].split('.')[0] + '.jpg'
        npfiles.append(imgpath + imagename)

for i, fname in enumerate(npfiles):
    img = rgb2gray( imread( fname ) )
    iblocks = getRndBlocks(img)
    for j, block in enumerate(iblocks):
        print block.shape
        hogDesc = hog( block, orientations=9, \
                   pixels_per_cell=(8, 8),\
                   cells_per_block=(2, 2) )
        ofname = str(i) + '_' + str(j)
        outFile = os.path.join(negoutpath,ofname)
        np.save(outFile, hogDesc)
    print 'Done ..', fname
