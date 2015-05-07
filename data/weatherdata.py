import urllib
from bs4 import BeautifulSoup

base_url = 'http://www.imdaws.com/WeatherAWSData.aspx?&FromDate=%s&ToDate=%s&State=%d&District=%s&Loc=%d&Time='

def parse(data):
    soup = BeautifulSoup(data, 'lxml')
    rows = soup.findAll( 'tr' )
    tables = soup.findAll( 'table' )
    rows = tables[1].findAll( 'tr' )
    pd = [ '\t'.join([ x.text for x in row.findAll('td') ])\
            for row in rows[1:] ]
    return '\n'.join(pd)

def getdata( frm, to , st, ds, loc ):
    url = base_url % ( frm, to, st, ds, loc )
    data = urllib.urlopen(url).read()
    pd = parse(data)
    with open( 'test.tsv', 'w' ) as outfile:
        outfile.write(pd)
    
#http://www.imdaws.com/WeatherAWSData.aspx?&FromDate=01/04/2015&ToDate=10/04/2015&State=25&District=CHENNAI&Loc=0&Time=
getdata( '01/04/2015', '10/04/2015', 25, 'CHENNAI', 0 )
