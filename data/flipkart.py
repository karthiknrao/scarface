import os
import urllib
from bs4 import BeautifulSoup
import time

reviewurl = '%s?rating=1,2,3,4,5&reviewers=all&start=%d'

def fetch(url):
    return urllib.urlopen(url).read()

def getpage1(url):
    data = fetch(url)
    outpath = url.split('/')[3]
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    with open( outpath + '/0.html', 'w' ) as outfile:
        outfile.write(data)
    soup = BeautifulSoup( data, 'lxml' )
    st = soup.findAll( 'div', 'line' )
    return int(st[0].findAll( 'strong' )[1].text)

def getpagen(url,n):
    data = fetch(url)
    outpath = url.split('/')[3]
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    with open( outpath + '/%d.html' % n, 'w' ) as outfile:
        outfile.write(data)

if __name__ == '__main__':
    
    prod_url = 'http://www.flipkart.com/asus-zenfone-5-a501cg/product-reviews/ITME6G47XYCW2PHS'
    url = reviewurl % ( prod_url, 0 )
    nprods = getpage1(url)
    
    for i in range(10,nprods,10):
        url = reviewurl % ( prod_url, i )
        getpagen(url,i)
        print 'Fetched ..', url
        time.sleep(5)
