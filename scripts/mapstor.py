import stem
import stem.connection

import time
import urllib2

from stem import Signal
from stem.control import Controller

import os
import math
import sys
import cv2
import numpy as np
import random


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}

oldIP = "0.0.0.0"
newIP = "0.0.0.0"

nbrOfIpAddresses = 3
secondsBetweenChecks = 2

burl = 'http://mt0.google.com/vt/lyrs=s@110&hl=en&x=%d&s=&y=%d&z=%d&s='

def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = '12345')
        controller.signal(Signal.NEWNYM)
        controller.close()

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
    url = burl % ( x, y, int(zoom) )
    destpath = os.path.join(destdir,str(x))
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    fname = os.path.join(destpath,str(y)+'.jpg')
    print(url,fname)
    data = request(url)
    with open(fname,'w') as outfile:
        outfile.write(data)
    return fname

def getwindowxy(x,y,zoom,destdir,width,outname):
    tiles = []
    for i in range( x - width, x + width + 1):
        for j in range( y - width, y + width + 1):
            fname = gettilexy(i,j,zoom,destdir)
            tiles.append(fname)
            time.sleep(2.0)
    winsize = (2*width + 1)*256
    buff = np.zeros((winsize,winsize,3))
    w = 2*width + 1
    for i in range(2*width+1):
        for j in range(2*width+1):
            img = cv2.imread(tiles[i*w + j])
            buff[j*256:j*256+256,i*256:i*256+256] = img
    cv2.imwrite(outname,buff)

def changeip():

    global newIP
    global oldIP
    if newIP == "0.0.0.0":
        renew_connection()
        newIP = request('http://icanhazip.com/')
    else:
        oldIP = newIP
        renew_connection()
        newIP = request("http://icanhazip.com/")

    seconds = 0


    while oldIP == newIP:
        time.sleep(secondsBetweenChecks)
        seconds += secondsBetweenChecks
        newIP = request("http://icanhazip.com/")
        print ("%d seconds elapsed awaiting a different IP address." % seconds)

    print ("")
    print ("newIP: %s" % newIP)

def changeiptry():
    while True:
        try:
            changeip()
            break
        except:
            continue
        
if __name__ == '__main__':
    root = 'maps'
    zoom = '19'
    width = 1
    
    destdir = os.path.join(root,zoom)

    locs = [ x.strip().split(',') for x in open(sys.argv[1]).readlines() ]
    
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    outname = 'fullimage_neg'

    changeiptry()
    i = 0
    for lat, lon in locs:
        x,y = xyfromlatlon(float(lat),float(lon),int(zoom))
        while True:
            try:
                getwindowxy(x,y,zoom,destdir,2,os.path.join(outname,lat + '_' + lon + '.jpg'))
                break
            except:
                changeiptry()
        i += 1
        if i % 5 == 0:
            changeiptry()
