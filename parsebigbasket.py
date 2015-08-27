from bs4 import BeautifulSoup
import glob
import os

def parse(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    prods = soup.findAll('li')
    products = [ x for x in prods if 'id' in x.attrs.keys() and 'product' in x['id'] ]
    dtuple = []
    for x in products:
        try:
            title = x.findAll('a')[0]['title'].encode('ascii','ignore' )
            price = x.findAll('div','uiv2-rate-count-avial')[0].text.encode('ascii','ignore' )
        except:
            continue
        dtuple.append((title,price))
    return [ '\t'.join(x) for x in dtuple ]

date = '%d-%02d-%02d'

months = { 6 : range(9,31),
           7 : range(1,32),
           8 : range(1,28) }

ddates = []
for key in months.keys():
    for x in months[key]:
        ddates.append( date % ( 2015, key, x ))
        
for dname in ddates:
    if not os.path.exists(dname):
        print dname
        continue
        
    files = glob.glob(dname+'/*')
    prices = []
    for x in files:
        print x
        prices += parse(x)
    
    with open( dname + '_parsed.tsv', 'w' ) as outfile:
        outfile.write( '\n'.join(prices) )
