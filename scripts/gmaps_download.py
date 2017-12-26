import urllib
import time
import os
import math
import sys
import pdb

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

if __name__ == '__main__':
    """
    root = sys.argv[1]
    zoom = sys.argv[2]
    lat = sys.argv[3]
    lon = sys.argv[4]
    width = int(sys.argv[5])
    """
    root = 'maps'
    zoom = '19'
    width = 1
    burl = 'http://mt0.google.com/vt/lyrs=s@110&hl=en&x=%d&s=&y=%d&z=%d&s='
    destdir = os.path.join(root,zoom)

    locs = [ x.strip().split(',') for x in open(sys.argv[1]).readlines() ]
    
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    for lat, lon in locs:
        x,y = xyfromlatlon(float(lat),float(lon),int(zoom))

        for i in range( x - width, x + width + 1 ):
            for j in range( y - width, y + width + 1 ):
                url = burl % ( i, j, int(zoom) )
                destpath = os.path.join(destdir,str(i))
                if not os.path.exists(destpath):
                    os.mkdir(destpath)
                fname = os.path.join(destpath,str(j)+'.jpg')
                print(url,fname)
                page = urllib.urlopen(url)
                data = page.read()
                with open(fname,'w') as outfile:
                    outfile.write(data)
                time.sleep(2.0)
    
