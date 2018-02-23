import urllib2
import time
import os
import math
import cv2
import numpy as np
import random
from multiprocessing import Pool
import quadkey
import requests
import sys

bingurl = 'http://t%d.ssl.ak.tiles.virtualearth.net/tiles/a%s.jpeg?g=6201&n=z&c4w=1'
googleurl = 'http://mt%d.google.com/vt/lyrs=s@110&hl=en&x=%d&s=&y=%d&z=%d&s='
veurl = 'http://ecn.t%d.tiles.virtualearth.net/tiles/a%s.jpeg?g=6216'
arcgisurl = 'http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%d/%d/%d/' # x,y interchanged

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

def geturlbing(x,y,zoom):
    qkey = quadkeyfromxy(x,y,zoom)
    server = random.choice([0,1,2,3])
    return bingurl % (server, qkey)

def geturlgoogle(x,y,zoom):
    server = random.choice([0,1,2,3])
    return googleurl % (server, x, y, zoom)

def geturlve(x,y,zoom):
    qkey = quadkeyfromxy(x,y,zoom)
    server = random.choice([0,1,2,3])
    return veurl % (server, qkey)

def geturlarcgis(x,y,zoom):
    return arcgisurl % (zoom, y, x)

def gettile(url,fname,destdir):
    if not os.path.exists(destdir):
        try:
            os.makedirs(destdir)
        except:
            pass
    proxies = {'http': 'http://127.0.0.1:3128'}
    if os.path.exists(fname):
        print('Done', url, fname)
        return fname
    proxy = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    try:
        page = urllib2.urlopen(url,timeout=2)
    except:
        return fname
    data = page.read()
    print(url,fname,len(data))
    if len(data) < 2000:
        return fname
    with open(fname,'w') as outfile:
        outfile.write(data)
    time.sleep(random.random()*1)
    return fname

def getgooglemaps(x,y,zoom,destdir):
    url = geturlgoogle(x,y,zoom)
    destpath = os.path.join(destdir,str(zoom),str(x))
    fname = os.path.join(destpath,str(y) + '.jpg')
    return gettile(url,fname,destpath)

def getbingmaps(x,y,zoom,destdir):
    url = geturlbing(x,y,zoom)
    destpath = os.path.join(destdir,str(zoom),str(x))
    qkey = quadkeyfromxy(x,y,zoom)
    fname = os.path.join(destpath,str(y) + '.' + qkey + '.jpg')
    return gettile(url,fname,destpath)

def getvemaps(x,y,zoom,destdir):
    url = geturlve(x,y,zoom)
    destpath = os.path.join(destdir,str(zoom),str(x))
    qkey = quadkeyfromxy(x,y,zoom)
    fname = os.path.join(destpath,str(y) + '.' + qkey + '.jpg')
    return gettile(url,fname,destpath)

def getarcgismaps(x,y,zoom,destdir):
    url = geturlarcgis(x,y,zoom)
    destpath = os.path.join(destdir,str(zoom),str(x))
    fname = os.path.join(destpath,str(y) + '.jpg')
    return gettile(url,fname,destpath)

def getpooltile(args):
    x,y,zoom,destdir,func = args
    return func(x,y,zoom,destdir)

def makebatch(lines,size):
    for i in range(0,len(lines),size):
        yield lines[i:i+size]

def getregion(lat,lon,size,zoom,destdir,func):
    startx, starty = xyfromlatlon(lat,lon,int(zoom))
    params = []
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    def getnotdownloaded(params):
        paramsremain = []
        for x,y,zoom,destdir,func in params:
            if 'google' in func.func_name:
                destpath = os.path.join(destdir,str(zoom),str(x))
                fname = os.path.join(destpath,str(y)+'.jpg')
            else:
                destpath = os.path.join(destdir,str(zoom),str(x))
                qkey = quadkeyfromxy(x,y,zoom)
                fname = os.path.join(destpath,str(y) + '.' + qkey + '.jpg')
    
            if not os.path.exists(fname):
                paramsremain.append((x,y,zoom,destdir,func))
            try:
                fstats = os.stat(fname)
                if fstats.st_size < 1500:
                    os.remove(fname)
                    paramsremain.append((x,y,zoom,destdir,func))
            except:
                pass
        return paramsremain
    
    for i in range(size):
        for j in range(size):
            x = startx + i
            y = starty + j
            params.append((x,y,zoom,destdir,func))

    pool = Pool(processes=5)
    for i in range(20):
        print( 'Pass ', i )
        params = getnotdownloaded(params)
        for batch in makebatch(params,200):
            try:
                pool.map(getpooltile,batch)
            except:
                continue

def getwindowxy(x,y,zoom,destdir,width,outname,func):
    tiles = []
    for i in range( x - width, x + width + 1):
        for j in range( y - width, y + width + 1):
            fname = func(i,j,zoom,destdir)
            tiles.append(fname)
    winsize = (2*width + 1)*256
    buff = np.zeros((winsize,winsize,3))
    w = 2*width + 1
    for i in range(2*width+1):
        for j in range(2*width+1):
            img = cv2.imread(tiles[i*w + j])
            buff[j*256:j*256+256,i*256:i*256+256] = img
    cv2.imwrite(outname,buff)

def getfromfile(fname,destdir,zoom,func):
    lines = [ x.strip().split() for x in open(fname).readlines() ]
    tilexys = [ (int(x[2]),int(x[3])) for x in lines ]
    #destpath = os.path.join(destdir,str(zoom))
    params = []
    #if not os.path.exists(destpath):
    #    os.makedirs(destpath)
        
    def getnotdownloaded(params):
        paramsremain = []
        for x,y,zoom,destdir,func in params:
            if 'gis' in func.func_name or 'google' in func.func_name:
                destpath = os.path.join(destdir,str(zoom),str(x))
                fname = os.path.join(destpath,str(y)+'.jpg')
            else:
                destpath = os.path.join(destdir,str(zoom),str(x))
                qkey = quadkeyfromxy(x,y,zoom)
                fname = os.path.join(destpath,str(y) + '.' + qkey + '.jpg')
    
            if not os.path.exists(fname):
                paramsremain.append((x,y,zoom,destdir,func))
            try:
                fstats = os.stat(fname)
                if fstats.st_size < 1500:
                    os.remove(fname)
                    paramsremain.append((x,y,zoom,destdir,func))
            except:
                pass
        return paramsremain
    
    for x,y in tilexys:
        params.append((x,y,zoom,destdir,func))

    pool = Pool(processes=3)
    for i in range(10):
        print( 'Pass ', i )
        params = getnotdownloaded(params)
        for batch in makebatch(params,200):
            try:
                pool.map(getpooltile,batch)
            except:
                continue

    
if __name__ == '__main__':
    
    
    fname = sys.argv[1]
    destdirn = os.path.join('arcgismaps/',os.path.basename(fname))
    getfromfile(fname,destdirn,15,getarcgismaps)
