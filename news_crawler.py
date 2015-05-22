import urllib
import re
import os
from bs4 import BeautifulSoup
import glob

"""
base_urls = [ 'http://www.firstpost.com/',
              'http://www.firstpost.com/category/politics',
              'http://www.firstpost.com/category/sports',
              'http://www.firstpost.com/category/india',
              'http://www.firstpost.com/category/world',
              'http://www.firstpost.com/category/business',
              'http://www.firstpost.com/category/living',
              'http://www.firstpost.com/category/bollywood' ]

regex = 'http://www.firstpost.com[0-9a-z\-\/]+[0-9]{7}\.html'

def fetch(url):
    return urllib.urlopen(url).read()

urls = []

for url in base_urls:
    data = fetch(url)
    matches = re.findall(regex,data)
    urls += matches

urls = list( set(urls) )
#open( 'news_urls','w').write('\n'.join(urls))
opath = 'news/'
if not os.path.exists( opath ):
    os.mkdir(opath)

for i,url in enumerate(urls):
    data = fetch(url)
    ofname = opath + str(i)
    with open( ofname, 'w' ) as outfile:
        outfile.write(data)
    print 'Done ..', i, url
"""

opath = 'parsed/'
if not os.path.exists( opath ):
    os.mkdir(opath)

def parse(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    texts = soup.findAll('p')
    textdata = [ x.text for x in texts ]
    return ' '.join(textdata)

files = glob.glob( 'news/*' )

for i, fname in enumerate(files):
    texts = parse(fname)
    ooname = opath + str(i)
    with open( ooname, 'w' ) as outfile:
        outfile.write(texts.encode('ascii','ignore'))
    print 'Done ..', i, fname
