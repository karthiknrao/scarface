import urllib
import time
import os
import math
import sys
import cv2
import numpy as np
import random
import glob

random.seed('123456')

def xyfromlatlon( lat_deg, lon_deg, zoom ):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = ((lon_deg + 180.0) / 360.0 * n)
    ytile = ( ( 1.0-math.log( math.tan( lat_rad )+( 1/math.cos(lat_rad)))/math.pi)/2.0*n)
    return ( xtile, ytile )

def latlonfromxy( x, y, zoom ):
    n = 2**zoom
    lon_deg = x/(n+0.0)*360.0 - 180.0
    lat_rad = math.atan( math.sinh( math.pi*( 1.0-(2.0*y)/n ) ) )
    lat_deg = math.degrees( lat_rad )
    return ( lat_deg, lon_deg )

def getlatlon(fname):
    basename = os.path.basename(fname)
    basename = basename.replace('.jpg','')
    lat , lon = [ float(x) for x in basename.split('_') ]
    return lat, lon

def getpatches(fname,outdir,t):
    lat, lon = getlatlon(fname)
    x,y = xyfromlatlon( lat, lon, 18 )
    dx = int((x - int(x))*256)
    dy = int((y - int(y))*256)
    #print(x,y,lat,lon,dx,dy)

    img = cv2.imread(fname)
    px = 256 + dx
    py = 256 + dy

    delx = 128
    dely = 128

    sx = px - delx
    sy = py - dely
    patch = img[sy:sy+256,sx:sx+256,:]
    patch = cv2.resize(patch,(224,224))
    oname = os.path.join(outdir,'0_' + t + os.path.basename(fname))
    cv2.imwrite(oname,patch)

    randpos = [ ( int(random.random()*200) - 100, int(random.random()*200) - 100 ) for i in range(10) ]
    i = 1
    for delx, dely in randpos:
        sx = px - 128 + delx
        sy = py - 128 + dely
        patch = img[sy:sy+256,sx:sx+256,:]
        patch = cv2.resize(patch,(224,224))
        oname = os.path.join(outdir,str(i) + '_' + t + os.path.basename(fname))
        print(oname)
        cv2.imwrite(oname,patch)
        i += 1

def getpatchesneg(fname,outdir,t):
    img = cv2.imread(fname)

    randpos = [ ( int(random.random()*256*4), int(random.random()*256*4) ) for i in range(40) ]

    i = 0
    for delx, dely in randpos:
        patch = img[delx:delx+256,dely:dely+256,:]
        patch = cv2.resize(patch,(224,224))
        oname = os.path.join(outdir,str(i) + '_' + t + os.path.basename(fname))
        cv2.imwrite(oname,patch)
        i += 1
        
if __name__ == '__main__':

    os.system( 'rm -r dataset18' )
    
    os.makedirs( 'dataset18/train/c2' )
    os.makedirs( 'dataset18/val/c2' )
    os.makedirs( 'dataset18/train/c1' )
    os.makedirs( 'dataset18/val/c1' )

    ## 1 brickkiln
    ## 0 random patches
    
    #### bing maps #####
    files = glob.glob( 'bingdata/1/*' )
    random.shuffle(files)
    ll = len(files)
    print(ll)
    train = files[:int(0.8*ll)]
    test = files[int(0.8*ll):]
    for fname in train:
        getpatches(fname,'dataset18/train/c2','bing')

    for fname in test:
        getpatches(fname,'dataset18/val/c2','bing')
        
    files = glob.glob( 'bingdata/0/*' )
    random.shuffle(files)
    ll = len(files)
    print(ll)
    train = files[:int(0.8*ll)]
    test = files[int(0.8*ll):]
    for fname in train:
        getpatchesneg(fname,'dataset18/train/c1','bing')

    for fname in test:
        getpatchesneg(fname,'dataset18/val/c1','bing')
    
    #### google maps ####
    files = glob.glob( 'data18/1/*' )
    random.shuffle(files)
    ll = len(files)
    print(ll)
    train = files[:int(0.8*ll)]
    test = files[int(0.8*ll):]
    for fname in train:
        getpatches(fname,'dataset18/train/c2','')

    for fname in test:
        getpatches(fname,'dataset18/val/c2','')
        
    files = glob.glob( 'data18/0/*' )
    random.shuffle(files)
    ll = len(files)
    print(ll)
    train = files[:int(0.8*ll)]
    test = files[int(0.8*ll):]
    for fname in train:
        getpatchesneg(fname,'dataset18/train/c1','')

    for fname in test:
        getpatchesneg(fname,'dataset18/val/c1','')
