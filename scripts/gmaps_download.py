import urllib
import time
import os
import math
import sys
import cv2
import numpy as np
import random
from multiprocessing import Pool

burl = 'http://mt%d.google.com/vt/lyrs=s@110&hl=en&x=%d&s=&y=%d&z=%d&s='

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

def gettilelatlon(lat,lon,zoom,destdir):
    x,y = xyfromlatlon(float(lat),float(lon),int(zoom))
    return gettilexy(x,y,zoom,destdir)

def gettilexy(x,y,zoom,destdir):
    server = [ 0, 1, 2 ]
    selected = random.choice(server)
    url = burl % ( selected, x, y, int(zoom) )
    destpath = os.path.join(destdir,str(x))
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    fname = os.path.join(destpath,str(y)+'.jpg')
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
    time.sleep(random.random()*5)
    return fname

def getpooltile(args):
    x = args[0]
    y = args[1]
    zoom = args[2]
    destdir = args[3]
    try:
        gettilexy(x,y,zoom,destdir)
    except:
        return
    return

def getwindowxy(x,y,zoom,destdir,width,outname):
    tiles = []
    for i in range( x - width, x + width + 1):
        for j in range( y - width, y + width + 1):
            fname = gettilexy(i,j,zoom,destdir)
            tiles.append(fname)
    winsize = (2*width + 1)*256
    buff = np.zeros((winsize,winsize,3))
    w = 2*width + 1
    for i in range(2*width+1):
        for j in range(2*width+1):
            img = cv2.imread(tiles[i*w + j])
            buff[j*256:j*256+256,i*256:i*256+256] = img
    cv2.imwrite(outname,buff)

def getbylocations(locsfile,root,zoom,width,outname):
    destdir = os.path.join(root,zoom)

    locs = [ x.strip().split(',') for x in open(sys.argv[1]).readlines() ]
    
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    if not os.path.exists(outname):
        os.mkdir(outname)
    
    params = []
    for lat, lon in locs:
        x,y = xyfromlatlon(float(lat),float(lon),int(zoom))
        for i in range(x - width, x + width + 1):
            for j in range(y - width, y + width + 1):
                params.append((i,j,zoom,destdir))
    
    pool = Pool(processes=3)
    for i in range(20):
        for batch in makebatch(params,10):
            pool.map(getpooltile,batch)

    for i, loc in enumerate(locs):
        lat = loc[0]
        lon = loc[1]
        x,y = xyfromlatlon(float(lat),float(lon),int(zoom))
        getwindowxy(x,y,zoom,destdir,width,os.path.join(outname,str(lat) + '_' + str(lon)+'.jpg'))

def getregion(root,zoom,loc,size):
    lat, lon = loc
    destdir = os.path.join(root,zoom)
    startx, starty = xyfromlatlon(lat,lon,int(zoom))
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    params = []
    for i in range(500):
        for j in range(500):
            x = startx + i
            y = starty + j
            params.append((x,y,zoom,destdir))
    random.shuffle(params)
    pool = Pool(processes=5)
    for i in range(10):
        for batch in makebatch(params,10):
            pool.map(getpooltile,batch)

def makebatch(lines,size):
    for i in range(0,len(lines),size):
        yield lines[i:i+size]
    
if __name__ == '__main__':
    
    lat = 30.162264
    lon = 75.378865
    
    locs = ( lat, lon )

    getregion('mapsregion18','18',locs,100)
