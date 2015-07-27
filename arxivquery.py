import urllib
from bs4 import BeautifulSoup
import sys,os
import requests

def progress_bar(count,bsize,tsize):
    sys.stdout.write( str(count*bsize) + '/' + str(tsize) + '\r' )
    sys.stdout.flush()

def parse(data):
    soup = BeautifulSoup(data,'lxml')
    entries = soup.findAll('entry')
    lnkpdf = ''
    records = []
    for entry in entries:
        title = entry.findAll('title')[0].text
        summary = entry.findAll('summary')[0].text
        links = entry.findAll('link')
        for link in links:
            try:
                if link['title'] == 'pdf':
                    lnkpdf = link['href']
                    break
                else:
                    continue
            except:
                continue
        records.append( (title.replace('\n',''),summary,lnkpdf) )
    return records

def fetch(lssrch):
    outpath = '_'.join(sys.argv[1:-1])
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for title, summary, link in lssrch:
        print 'Fetching..',title,link
        req = urllib.urlopen(link).read()
        fname = os.path.join(outpath,title.replace(' ','_')+'.pdf')
        urllib.urlretrieve( link, fname, progress_bar )
        """
        with open( os.path.join(outpath,title.replace(' ','_')+'.pdf') , 'w' ) as outfile:
            outfile.write(req.text)
        """
        print title, link
        
base_url = 'http://export.arxiv.org/api/query?search_query=all:%s&start=%d'
srch_results = []
for i in range(0,int(sys.argv[-1])+10,10):
    url = base_url % ( '+'.join(sys.argv[1:-1]), i )
    data = urllib.urlopen(url).read()
    srch_results += parse(data)

fetch(srch_results)
