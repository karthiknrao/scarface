import urllib
import os
#/datafeed/AUDCAD/2014/09/12/21h_ticks.bi5
"""
symbol = [ 'XAGUSD', 'XAUUSD', 'BRENTCMDUSD', 'LIGHTCMDUSD', 'EURUSD',
           'EURGBP', 'EURJPY', 'USDJPY', 'AUDUSD','USDRUB',
           'GBPUSD', 'USDJPY' ]
"""
symbol =   [  'BRAIDXBRL', 'USAMJRIDXUSD', 'USA30IDXUSD',
           'USATECHIDXUSD', 'JPNIDXJPY', 'APPLUSAUSD', 'AMAZUSAUSD', 'BOAUSAUSD',
           'COPAUSAUSD', 'CISCUSAUSD', 'CHEVUSAUSD', 'DELLUSAUSD', 'DISNUSAUSD',
           'EBAYUSAUSD', 'GEELUSAUSD', 'GEMOUSAUSD', 'GOOGUSAUSD', 'HOMEUSAUSD',
           'HEPAUSAUSD', 'IBMUSAUSD', 'INTCUSAUSD', 'JOJOUSAUSD', 'JPMCUSAUSD',
           'COCOUSAUSD', 'MCDNUSAUSD','3MCOUSAUSD', 'MSFTUSAUSD', 'ORCLUSAUSD',
           'YHOOUSAUSD','WMSUSAUSD']

stocks = [ 'APPLUSAUSD', 'AMAZUSAUSD', 'BOAUSAUSD', 'COPAUSAUSD', 'CISCUSAUSD',
           'CHEVUSAUSD', 'DELLUSAUSD', 'DISNUSAUSD', 'EBAYUSAUSD', 'GEELUSAUSD',
           'GEMOUSAUSD', 'GOOGUSAUSD', 'HOMEUSAUSD', 'HEPAUSAUSD', 'IBMUSAUSD',
           'INTCUSAUSD', 'JOJOUSAUSD', 'JPMCUSAUSD', 'COCOUSAUSD', 'MCDNUSAUSD',
           '3MCOUSAUSD', 'MSFTUSAUSD', 'ORCLUSAUSD', 'PRGAUSAUSD', 'PHMOUSAUSD',
           'STARUSAUSD', 'ATTUSAUSD', 'UNPSUSAUSD', 'WMSUSAUSD', 'EXXOUSAUSD',
           'YHOOUSAUSD' ]


class Dukascopy():
    def __init__( self ):
        self.base = 'http://www.dukascopy.com/datafeed/%s/%d/%.2d/%.2d/%.2dh_ticks.bi5'
        self.pathbase = ''
        self.daysInMonth = [ 31, 29, 31, 30, 31, 30,\
                             31, 31, 30, 31, 30, 31 ]
    def setItem( self, item ):
        self.item = item

    def download( self, year, mon, date, hr ):
        url = self.base % ( self.item, year, mon,\
                            date, hr )
        path = '/'.join( [ self.pathbase, self.item,
                           str( year ), str( mon ),\
                           str( date ) ] )

        self.checkPath( path )
        filepath = path + '/%.2dh_ticks.bi5' % hr
        if os.path.exists( filepath ):
            return
        page = urllib.urlopen( url )
        data = page.read()
        print url, len(data)
        with open( filepath , 'w' ) as outfile:
            outfile.write( data )
    
    def day( self, year, mon, date ):
        for hr in range( 24 ):
            self.download( year, mon, date, hr )

    def downMonth( self, year, mon ):
        for i in range( self.daysInMonth[mon] ):
            self.day( year, mon, i + 1 )

    def downYear( self, year ):
        for i in range( 12 ):
            self.downMonth( year, i )

    def setPath( self, pathbase ):
        self.pathbase = pathbase

    def checkPath( self, path ):
        pathbr = path.split( '/' )
        pathlist = [ '/'.join( pathbr[0:i] ) for i in\
                     range(1, len( pathbr ) + 1 )]
        for path in pathlist:
            if not os.path.exists( path ):
                os.mkdir( path )

if __name__ == '__main__':
    dkp = Dukascopy()
    dkp.setPath( 'FinancialData' )
    for sym in stocks:
        dkp.setItem( sym )
        dkp.downMonth( 2014, 7 )
