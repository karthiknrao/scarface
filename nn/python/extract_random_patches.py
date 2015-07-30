import sys
import glob
import os
import cv2
import random from random

files = glob.glob(sys.argv[1])
files = [ x.strip() for x in open(sys.argv[1]).readlines() ]
outpath = sys.argv[2]
if not os.path.exists(outpath):
    os.mkdir(outpath)
    
for fname in files:
    img = cv2.imread(fname)
    print fname
    (x,y) = img.shape
     x_ = x - 100
     y_ = y - 100
     pos = [ ( int(random()*x_), int(random()*y_) ) for i in range(9) ]
     filename = os.path.basename(fname)
     for i,x in enumerate(pos):
         imgb = img[x[0]:x[0]+100,x[1]:x[1]+100]
         oname = str(i) + '_' + filename
         cv2.imwrite(os.path.join(outpath,oname),imgb)
    
