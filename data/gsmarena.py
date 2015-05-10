import os,sys
from bs4 import BeautifulSoup
import glob
from json import JSONEncoder
import re,urllib

def fetch(url):
    return urllib.urlopen(url).read()

def parsehome(url):
    data = fetch(url)
    soup = BeautifulSoup(data,'lxml')
    brands = soup.findAll('div', { 'id' : 'brandmenu' })[0]
    urls = []
    for brand in brands.findAll('li'):
        print brand
        urls += [brand.findAll('a')[0]['href']]
    return urls

def getpages(url):
    data = fetch(url)
    soup = BeautifulSoup(data,'lxml')
    pages = soup.findAll('div','nav-pages')
    if len(pages) > 0:
        urls = [ x['href'] for x in pages[0].findAll('a') ]
        return map(lambda x: domain + x, urls )
    else:
        return []

def _parsebrands(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    parts = soup.findAll('div','makers')
    urls = []
    for part in parts:
        prods = part.findAll('li')
        for prod in prods:
            urls.append(prod.findAll('a')[0]['href'])
    return urls

def parsebrands(dirname):
    paths = glob.glob('crawl/*')
    for path in paths:
        files = glob.glob(path+'/*')
        for fname in files:
            urls = _parsebrands(fname)
            furls = [ '\t'.join(x) for x in zip( [fname]*len(urls), urls ) ]
            with open( 'parsedurls.tsv', 'a' ) as outfile:
                outfile.write( '\n'.join(furls) + '\n' )
            print fname

"""
paginated = '%s-f-%s-0-p%d.php'
domain = 'http://www.gsmarena.com/'
urls = parsehome(domain)
print urls
outpath = 'crawl'
for url in urls:
    print url
    brand = url.replace( '-', '' )
    dest = os.path.join(outpath,brand)
    if not os.path.exists( dest ):
        os.mkdir(dest)
    xurls = getpages(domain+url) + [domain+ url]
    for i,xurl in enumerate(xurls):
        data = fetch(xurl)
        with open( dest + '/' + str(i) + '.html','w') as outfile:
            outfile.write(data)
        print xurl
"""

parsebrands('crawl')
