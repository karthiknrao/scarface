from bs4 import BeautifulSoup
import urllib2

class GoogleSch():
    base_url = 'http://scholar.google.com/scholar?q=%s&hl=en'

    def __init__( self, qry ):
        self.url = self.base_url % ( '+'.join(qry.split()) )
        self.headers = { 'User-agent' :\
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36' }
    
    def fetch( self, url ):
        req = urllib2.Request(url,None,self.headers)
        return urllib2.urlopen(req).read()

    def parse( self ):
        data = self.fetch(self.url)
        soup = BeautifulSoup(data,'lxml')
        results = soup.findAll('div','gs_r')
        for result in results:
            try:
                link = result.findAll('div','gs_md_wp gs_ttss')[0].findAll('a')[0]['href']
            except:
                link = 'NA'
            try:
                title = result.findAll('h3','gs_rt')[0].text
            except:
                title = 'NA'
            print title, link

if __name__ == '__main__':
    gsch = GoogleSch()
    gsch.parse()
