import glob
from bs4 import BeautifulSoup

annotatepath = '/home/indix/Documents/data/VOCdevkit/VOC2012/Annotations/*'
imgpath = '/home/indix/Documents/data/VOCdevkit/VOC2012/JPEGImages/'

files = glob.glob( annotatepath )

def parse(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    names = [ x.text.encode('ascii', 'ignore') for x in soup.findAll( 'name' ) ]
    return [ x.lower() for x in names ]

npfiles = []
for fname in files:
    tags = parse(fname)
    if 'person' not in tags:
        imagename = fname.split('/')[-1].split('.')[0] + '.jpg'
        npfiles.append(imgpath + imagename)
        
print len(npfiles)
