import glob
from bs4 import BeautifulSoup

def parseFile(fname):
    data = open(fname).read()
    soup = BeautifulSoup( data, 'lxml' )
    brand = soup.findAll('div','brand_name')[0].text
    title = soup.findAll('h2','mega_prod-name')[0].text
    price = soup.findAll('span','mega_price ')[0].text
    precat = soup.findAll('div','path_for_current_product row')[0].findAll('a')
    cat = ' > '.join([ x.text.encode('ascii', 'ignore' ) for x in precat ])
    info = [ title, brand, price, cat ]
    cleaninfo = [ x.replace( '\t', '' ) for x in info ]
    info = [ x.replace( '\n', '' ) for x in cleaninfo ]
    return [ x.encode('ascii', 'ignore' ).strip() for x in info ]

files = glob.glob( 'ibf/*.html' )
for fname in files:
    print '\t'.join([fname] + parseFile(fname))
