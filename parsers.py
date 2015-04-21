from bs4 import BeautifulSoup

class Parser():
    def __init__( self, data ):
        self.soup = BeautifulSoup( data, 'lxml' )

    def parse( self, z, y ):
        texts = list( set( [ x.text for x in \
                    self.soup.findAll( z, y ) ] ) ) 
        return (' '.join(texts)).encode('ascii', 'ignore')

parsers = {
    'zeenews.india.com' : lambda x : Parser(x).parse('div','field-item even'),
    'www.financialexpress.com' : lambda x : Parser(x).parse( 'div', 'main-story' ),
    'articles.economictimes.indiatimes.com' : lambda x : Parser(x).parse( 'div', 'area' ),
    'indianexpress.com' : lambda x : Parser(x).parse( 'div', 'main-body-content' ),
    'timesofindia.indiatimes.com' : lambda x : Parser(x).parse( 'div', 'Normal' ),
    'indiatoday.intoday.in' : lambda x : Parser(x).parse( 'div', 'mediumcontent' ),
    'www.ndtv.com' : lambda x : Parser(x).parse( 'div', 'ins_storybody' ),
    'www.livemint.com' : lambda x : Parser(x).parse( 'div', 'p' ),
    'www.thehindu.com' : lambda x : Parser(x).parse( 'div', 'articleLead' ),
    'www.firstpost.com' : lambda x : Parser(x).parse( 'div', 'fullCont1' ),
    'www.oneindia.com' : lambda x : Parser(x).parse( 'div', 'ecom-ad-content' )
}
        
