import sys
import os
from bs4 import BeautifulSoup
import urllib

def fetch(url):
    return urllib.urlopen(url).read()

class BloomBerg():
    def __init__(self):
        self.urls = [ 
            'http://www.bloomberg.com/technology',
            'http://www.bloomberg.com/markets',
            'http://www.bloomberg.com/politics'
            ]

    def getlinks(self):
        links = []
        for url in self.urls:
            data = fetch(url)
            links += self.parse(data,url)
        return '\n'.join([ '\t'.join(x) for x in links ])
            
    def parse(self,data,url):
        soup = BeautifulSoup(data,'lxml')
        links = soup.findAll('a')
        output = [ ( url + '/' + x['href'], x.text ) for x in links \
                   if 'articles' in x['href'] and x.text.replace(' ','') != '' ]
        return output

class BusinessInsider():
    def __init__(self):
        self.urls = [ 
            'http://www.businessinsider.com/sai',
            'http://www.businessinsider.com/clusterstock',
            'http://www.businessinsider.com/politics'
        ]

    def getlinks(self):
        links = []
        for url in self.urls:
            data = fetch(url)
            links += self.parse(data,url)
        return '\n'.join([ '\t'.join(x) for x in links ])
            
    def parse(self,data,url):
        soup = BeautifulSoup(data,'lxml')
        links = soup.findAll('a')
        output = [ ( x['href'], x.text ) for x in links\
                   if 'href' in x.attrs and 'www.businessinsider.in' in x['href'] and x.text != '' ]
        return output

class VentureBeat():
    def __init__(self):
        self.urls = [ 'http://venturebeat.com/category/deals/page/%d' % i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/entrepreneur/page/%d' % i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/dev/page/%d' % i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/enterprise/page/%d' % i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/business/page/%d' % i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/mobile/page/%d' %i for i in range(1,5) ] +\
                    [ 'http://venturebeat.com/category/media/page/%d' % i for i in range(1,5) ]
        
    def getlinks(self):
        links = []
        for url in self.urls:
            data = fetch(url)
            links += self.parse(data,url)
        return '\n'.join([ '\t'.join(x) for x in links ])
            
    def parse(self,data,url):
        soup = BeautifulSoup(data,'lxml')
        links = soup.findAll('a')
        output = [ ( x['href'], x['title'] ) for x in links\
                   if 'href' in x.attrs and 'title' in x.attrs and 'Permalink to' in x['title'] ]
        return [ (x[0],x[1].replace('Permalink to ','')) for x in output ]

site = BloomBerg()
print site.getlinks()
site = BusinessInsider()
print site.getlinks()
