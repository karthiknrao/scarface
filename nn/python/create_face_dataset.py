import sys
import os
import cv2
import glob

files = glob.glob(os.path.join(sys.argv[1],'*'))
outpath = sys.argv[2]
if not os.path.exists(outpath):
    os.mkdir(outpath)
posh = [ (25,'l'), (75,'c'), (125,'r') ]
posw = [ (25,'t'), (75,'c'), (125,'b') ]
pairs = [ (x[0],y[0],x[1]+y[1]) for x in posh for y in posw ]
for fname in files:
    print 'Done ..', fname
    filename = os.path.basename(fname)
    img = cv2.imread(fname)
    imgblocks = []
    for x, y, xy in pairs:
        imgblocks.append((img[x:x+100,y:y+100],xy))
    for block, pos in imgblocks:
        destname = os.path.join(outpath,filename.split('.')[0]+'_'+pos+'.jpg')
        cv2.imwrite(destname,block)
