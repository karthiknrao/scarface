from bs4 import BeautifulSoup
import requests
import sys

class GoogleNews():
    def __init__( self, qry ):
        self.base = 'https://www.google.co.in/search?q=%s+site:arxiv.org&start=%d'
        self.qry = '+'.join(qry)
        self.headers = { 'User-agent' :\
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36' }
        self.data = []
        
    def fetch( self, pages ):
        for page in range(pages):
            num = page*10
            url = self.base % ( self.qry, num )
            self.data.append( requests.get( url, headers=self.headers ).text )

    def _parse( self, data ):
        soup = BeautifulSoup( data, 'lxml' )
        x = soup.findAll( 'li', 'g' )
        return [ y.findAll('h3','r')[0].text for y in x ]

    def parse( self ):
        urls = []
        for data in self.data:
            urls += self._parse(data)
        return urls

if __name__ == '__main__':
    gnews = GoogleNews( sys.argv[1:] )
    gnews.fetch( 10 )
    print '\n'.join(gnews.parse())
