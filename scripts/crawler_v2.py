from gevent import monkey
monkey.patch_all()
import urllib2
import unirest
import os
import glob
import re
import StringIO
from PIL import Image
import md5

opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'localhost:8080'}))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]             
                                        
urllib2.install_opener(opener)           

import sys

from gevent.pool import Pool

def batch(givenList, batchSize):
    consumedUpto = 0
    while consumedUpto < len(givenList):
        currBatch = []
        while len(currBatch) < batchSize and consumedUpto < len(givenList):
            currBatch.append(givenList[consumedUpto])
            consumedUpto += 1
        yield currBatch

class BatchFetcher:
    def __init__(self, key):
        self.cleanup()
        self.key = key

    def fetch(self, url):
        try:
            if tor:
                res = urllib2.urlopen(url[1], timeout=10)
                htmlPage = res.read()                    
                self.htmlPages.append((url, htmlPage))
                #sys.stderr.write("FETCHED\t" + url[1] + "\n")
            else:
                crawleraEndpoint = "https://crawlera.p.mashape.com/fetch?url="
                quoteURL = urllib2.quote(url[1])
                fetchurl = crawleraEndpoint + quoteURL
                response = unirest.get(fetchurl, headers={"X-Mashape-Key": self.key})
                self.htmlPages.append((url, response))
        except Exception as e:
            sys.stderr.write("ERROR\t" + url[1] + "\t" +  str(url[0]) + "\t" + str(e) + "\n")
    
    def cleanup(self):
        self.htmlPages = []
        
    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

def crawl( batchFile, outpath ):
    with open(batchFile) as inputFile:
        lines = [ x.strip() for x in inputFile.readlines() ]
    #records = zip( range(len(lines)), [i.strip() for i in lines] )
    urlHashFile = dest + '/' + batchFile.split('/')[-1] +  '_urlhash'
    """
    recordsToDownload = [ records[i] for i in range(len(records)) \
                              if not os.path.exists( outpath +\
                                                         '/' + str(i) + '.jpg' ) ]
    """
    if os.path.exists(urlHashFile):
        doneUrls = [ x.strip().split('\t')[0] for x in open( urlHashFile ).readlines() ]
    else:
        doneUrls = []
    #recordsToDownload = [ x for x in records if x[1] not in doneUrls ]
    notdone = list(set(lines).difference(set(doneUrls)))
    print len(set(lines)), len(set(doneUrls)), len(set(notdone))
    recordsToDownload = zip( range(len(notdone)), [i.strip() for i in notdone] )
    batchFetcher = BatchFetcher(key)
    for currBatch in batch(recordsToDownload, batchSize):
        currWebpages = batchFetcher.fetchBatch(currBatch, poolSize)
        mappingFile = open( urlHashFile, 'a' )
        for record in currWebpages:
            url = record[0][1]
            indx = record[0][0]
            if tor:
                htmlPage = record[1]
            else:
                htmlPage = record[1].body
            #outputFilename = outpath + "/" + str(indx) + ".jpg"
            try:
                imfile = StringIO.StringIO(htmlPage)
                    #print type(imfile)
                im = Image.open(imfile)
                ext=im.format
                m = md5.new()
                try:
                   m.update(im.tostring())
                except:
                   print url
                   pass
                try:  
                   m.update(im.tostring())  
                except:
                   print '****FUCK-ERRROR',url
                   continue
                img_md5sum = m.hexdigest()
                outputFilename = outpath + "/" + img_md5sum + '.' + ext
                mappingFile.write( url + '\t' + outputFilename + '\n' )
                with open(outputFilename, 'w') as outputFile: 
                   outputFile.write(htmlPage)
            except:
                print sys.exc_info()[0]
                continue
        mappingFile.close()
            #sys.stderr.write("SUCCESS\t" + url + "\t" + outputFilename + "\n" )

def checkFiles( outpath ):
    files = glob.glob( outpath + '/' + '*.jpg' )
    recrawl = []
    for fname in files:
        meta = os.stat( fname )
        size = meta.st_size
        if size < 500:
            recrawl.append( fname )
    print 'Found ', len(recrawl), ' files for recrawl'
    indx = [ int(re.findall( '[0-9]+', x.split('/')[-1] )[0]) for x in recrawl ]
    for i in indx:
        path = outpath + '/' + str(i) + '.jpg'
        os.remove(path)
    return True

def crawlMain(src, dest):
    files = glob.glob( src + '/*' )
    outpath = [dest +  '/' + x.split('/')[-1] for x in files ]
    batches = zip( files, outpath )
    for batchFile, outpath in batches:
        print 'Crawling .. ', batchFile
        if not os.path.exists( outpath ):
            os.mkdir( outpath )
        for i in range(1):
            crawl( batchFile, outpath )
        checkFiles( outpath )
        for i in range(1):
            crawl( batchFile, outpath )
        os.system( 'touch ' + outpath + '/Done' )
           
if __name__ == '__main__':
    tor = True
    key = sys.argv[1]
    batchSize = int(sys.argv[2])
    poolSize = int(sys.argv[3])
    src = sys.argv[4]
    dest = sys.argv[5]
    if src[-1] == '/':
        src = src[:-1]
    if dest[-1] == '/':
        dest = dest[:-1]
    crawlMain(src, dest)
