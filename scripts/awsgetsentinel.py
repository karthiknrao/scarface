import sys
import os
import requests
import argparse
import xmltodict
import time

urlyear = 'http://sentinel-s2-l1c.s3.amazonaws.com/?delimiter=/&prefix=tiles/%d/%s/%s/%d/'
urlmonth = 'http://sentinel-s2-l1c.s3.amazonaws.com/?delimiter=/&prefix=tiles/%d/%s/%s/%d/%d/'
urlday = 'tiles/%d/%s/%s/%d/%d/%d/'
urlbase = 'http://sentinel-s2-l1c.s3.amazonaws.com/?delimiter=/&prefix='
urlimage = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/43/P/GQ/2018/1/14/0/B04.jp2'
urlimagebase = 'http://sentinel-s2-l1c.s3.amazonaws.com/'

imagefiles = [ 'B%.2d.jp2' % i for i in range(1,13) ] + [ 'B8A.jp2' ]
files = imagefiles + [ 'TCI.jp2', 'metadata.xml', 'preview.jp2', 'preview.jpg', 'productInfo.json', 'tileInfo.json' ] +\
        [ 'auxiliary/ECMWFT', 'qi/FORMAT_CORRECTNESS.xml', 'qi/GENERAL_QUALITY.xml', 'qi/GEOMETRIC_QUALITY.xml', 'qi/SENSOR_QUALITY.xml' ]
qifiles = [ 'qi/MSK_DEFECT_B%.2d.gml' % i for i in range(1,13) ] + [ 'qi/MSK_DEFECT_B8A.gml' ] +\
          [ 'qi/MSK_DETFOO_B%.2d.gml' % i for i in range(1,13) ] + [ 'qi/MSK_DETFOO_B8A.gml' ] +\
          [ 'qi/MSK_NODATA_B%.2d.gml' % i for i in range(1,13) ] + [ 'qi/MSK_NODATA_B8A.gml' ] +\
          [ 'qi/MSK_SATURA_B%.2d.gml' % i for i in range(1,13) ] + [ 'qi/MSK_SATURA_B8A.gml' ] +\
          [ 'qi/MSK_TECQUA_B%.2d.gml' % i for i in range(1,13) ] + [ 'qi/MSK_TECQUA_B8A.gml' ]
files += qifiles

wgetcmd = 'wget --limit-rate=%dK -c -P %s %s'

def fetch(url):
    page = requests.get(url)
    return page.text

def parse(page):
    doc = xmltodict.parse(page)
    urls = []
    if len(doc['ListBucketResult']['CommonPrefixes']) > 1:
        for x in doc['ListBucketResult']['CommonPrefixes']:
            urls.append(x['Prefix'])
    else:
        urls.append(doc['ListBucketResult']['CommonPrefixes']['Prefix'])
    return urls

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument( '-y', action='store', dest='year', help='year', type=int )
    p.add_argument( '-utm', action='store', dest='utm', help='utm', type=int )
    p.add_argument( '-lc', action='store', dest='lc', help='latitude tile' )
    p.add_argument( '-c', action='store', dest='c', help='tile' )
    p.add_argument( '-m', action='store', dest='m', help='month', type=int )
    p.add_argument( '-l' , action='store', dest='l', help='list', type=int )
    p.add_argument( '-d' , action='store', dest='d', help='day', type=int )
    
    outdir = 'images'
    
    args = p.parse_args()
    if args.m == None:
        url = urlyear % ( args.utm, args.lc, args.c, args.year )
    else:
        url = urlmonth % ( args.utm, args.lc, args.c, args.year, args.m )
        
    if args.l == None:
        print(parse(fetch(url)))
        sys.exit(0)

    if args.m == None:
        months = parse(fetch(url))
        urls = []
        for month in months:
            murl = urlbase + month
            urls += parse(fetch(murl))
    else:
        if args.d == None:
            urls = parse(fetch(url))
        else:
            urls = [ urlday % ( args.utm, args.lc, args.c, args.year, args.m, args.d ) ]
        
    passurls = []
    for url in urls:
        furl = urlbase + url
        passurls += parse(fetch(furl))

    for passurl in passurls:
        fullpassurl = urlimagebase + passurl
        for fname in files:
            fileurl = fullpassurl + fname
            dname = '/'.join(fileurl.split('/')[:-1]).replace('http://sentinel-s2-l1c.s3.amazonaws.com/tiles/','')
            destdir = os.path.join(outdir,dname)
            fnameo = os.path.basename(fileurl)
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            outname = os.path.join(destdir,fnameo)
            if os.path.exists(outname):
                print('Done ', outname)
                continue
            now = time.localtime()
            if now.tm_hour >= 19 and now.tm_hour <= 23:
                downcmd = wgetcmd % ( 1000, destdir, fileurl )
            elif now.tm_hour >= 0 and now.tm_hour <= 10:
                downcmd = wgetcmd % ( 2000, destdir, fileurl )
            else:
                downcmd = wgetcmd % ( 1500, destdir, fileurl )
            os.system(downcmd)
        
