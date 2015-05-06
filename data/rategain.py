import sys
import urllib
from bs4 import BeautifulSoup
import os
import re

class YearPage():
    def __init__( self, data ):
        self.soup = BeautifulSoup( data, 'lxml' )

    def parse( self ):
        links = self.soup.findAll( 'a' )
        return [ x['href'] for x in links[:-1] ]

url = 'http://ratedata.gaincapital.com/2014/'

links = YearPage( urllib.urlopen( url ).read() ).parse()

class MonthParser():
    def __init__( self, data ):
        self.soup = BeautifulSoup( data, 'lxml' )

    def parse( self ):
        links = self.soup.findAll( 'a' )
        return [ x['href'] for x in links ]

year = re.findall( '[0-9]+', url )[0]
if not os.path.exists( year ):
    os.mkdir( year )

cmd = 'wget --directory-prefix=%s -O "%s" "%s"'
for i, link in enumerate(map( lambda x: url + x + '/', links )):
    month = re.findall( '[A-Za-z]+', links[i] )[0]
    path = os.path.join( year, month )
    if not os.path.exists( path ):
        os.mkdir( path )
    datalinks = MonthParser( urllib.urlopen( link ).read() ).parse()
    dlinks = map( lambda x: link + x, datalinks )
    for j, dlink in enumerate(dlinks):
        oname = datalinks[j][2:]
        spath = os.path.join( path, oname )
        if os.path.exists( spath ):
            print dlink
            continue
        data = urllib.urlopen( dlink ).read()
        open( spath, 'w' ).write( data )
        print dlink
