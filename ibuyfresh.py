import urllib
from bs4 import BeautifulSoup
import os

base_url = 'http://www.ibuyfresh.com/view_product?id=%d'
maxprods = 8540

datapath = 'ibf'

def fetch(url):
    return urllib.urlopen(url).read()

def crawl():
    for i in range(maxprods):
        pid = i + 1
        url = base_url % pid
        filepath = datapath + '/' + str(pid) + '.html'
        if not os.path.exists(filepath):
            data = fetch(url)
            open(filepath,'w').write(data)
            print 'Crawled ',pid,filepath

if __name__ == '__main__':
    if not os.path.exists( datapath ):
        os.mkdir( datapath )

    crawl()
