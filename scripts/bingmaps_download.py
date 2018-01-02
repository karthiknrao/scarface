import urllib
import time
import os
import math
import sys
import cv2
import numpy as np
import random
from multiprocessing import Pool
import quadkey

burl = 'https://t%d.ssl.ak.tiles.virtualearth.net/tiles/a%s.jpeg?g=6201&n=z&c4w=1'
gurl = 'http://mt%d.google.com/vt/lyrs=s@110&hl=en&x=%d&s=&y=%d&z=%d&s='

def xyfromlatlon( lat_deg, lon_deg, zoom ):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = ((lon_deg + 180.0) / 360.0 * n)
    ytile = ( ( 1.0-math.log( math.tan( lat_rad )+( 1/math.cos(lat_rad)))/math.pi)/2.0*n)
    return ( int(xtile), int(ytile) )

def latlonfromxy( x, y, zoom ):
    n = 2**zoom
    lon_deg = x/(n+0.0)*360.0 - 180.0
    lat_rad = math.atan( math.sinh( math.pi*( 1.0-(2.0*y)/n ) ) )
    lat_deg = math.degrees( lat_rad )
    return ( lat_deg, lon_deg )

def quadkeyfromlatlon(lat_deg, lon_deg, zoom):
    qk = quadkey.from_geo((lat, lon), zoom)
    return qk.key

def quadkeyfromxy(x, y, zoom):
    lat, lon = latlonfromxy(x, y, zoom)
    qk = quadkey.from_geo((lat, lon), zoom)
    return qk.key

def geturl(qkey):
    server = random.choice([0,1,2,3])
    url = burl % ( server, qkey )
    return url

def gmapsurl(x,y,zoom):
    server = random.choice([ 0,1,2,3])
    url = gurl % ( server, x, y, zoom )
    return url

def gettilexy(qkey,x,y,destdir):
    server = random.choice([0,1,2,3])
    url = burl % ( server, qkey )
    destpath = os.path.join(destdir,str(x))
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    fname = os.path.join(destpath,str(y) + '.' + qkey +'.jpg')
    if os.path.exists(fname):
        print('Done',url,fname)
        return fname
    proxies = {'http': 'http://127.0.0.1:3128'}
    page = urllib.urlopen(url, proxies=proxies)
    data = page.read()
    print(url,fname,len(data))
    if len(data) < 2000:
        return fname
    with open(fname,'w') as outfile:
        outfile.write(data)
    time.sleep(random.random()*3)
    return fname

def getpooltile(args):
    qkey = args[0]
    x = args[1]
    y = args[2]
    destdir = args[3]
    try:
        gettilexy(qkey,x,y,destdir)
    except:
        return
    return

def getwindowxy(x,y,zoom,destdir,width,outname):
    tiles = []
    for i in range( x - width, x + width + 1):
        for j in range( y - width, y + width + 1):
            qdkey = quadkeyfromxy(i, j, zoom)
            fname = gettilexy(qdkey,i,j,destdir)
            tiles.append(fname)
    winsize = (2*width + 1)*256
    buff = np.zeros((winsize,winsize,3))
    w = 2*width + 1
    for i in range(2*width+1):
        for j in range(2*width+1):
            img = cv2.imread(tiles[i*w + j])
            buff[j*256:j*256+256,i*256:i*256+256] = img
    cv2.imwrite(outname,buff)


if __name__ == '__main__':
    lat = 31.796799
    lon = 75.389562
    zoom = 18
    destdir = os.path.join('bingmaps',str(zoom))
    oname = 'bingfull'

    if not os.path.exists(oname):
        os.mkdir(oname)
        
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    locs = [ map(float,x.strip().split(',')) for x in open(sys.argv[1]).readlines() ]
    params = []
    for lat, lon in locs:
        startx, starty = xyfromlatlon( lat, lon, zoom )
        for i in range(-1,2):
            for j in range(-1,2):
                x = startx + i
                y = starty + j
                qdkey = quadkeyfromxy(x, y, zoom)
                params.append((qdkey,x,y,destdir))

    for param in params:
        getpooltile(param)

    for lat,lon in locs:
        startx, starty = xyfromlatlon( lat, lon, zoom )
        getwindowxy(startx,starty,zoom,destdir,1,oname)
