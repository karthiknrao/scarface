from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
import pdb

class GoogleImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.base_url = 'https://www.google.com/search?q=%s&tbm=isch'
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry) )
        self.browser.get(url)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'div', 'rg_di rg_el ivg-i' )
        print len(x)
        imgs = [ y.findAll('a')[0]['href'] for y in x ]
        imgurls = [ ( x.split('imgurl=')[1].split('&')[0],\
                    x.split('imgurl=')[1].split('&')[1].replace('imgrefurl=','') )\
                    for x in imgs ]
        return imgurls

    def stop():
        browser.quit()
        display.stop()

if __name__ == '__main__':
    gimgs = GoogleImages()
    urls =  gimgs.crawl(sys.argv[1:])
    with open( '_'.join(sys.argv[1:]) , 'w' ) as outfile:
        for x in urls:
            outfile.write( '\t'.join(x) + '\n' )

"""
outdir = sys.argv[1]
if not os.path.exists(outdir):
    os.mkdir(outdir )
headers = { 'User-agent' :
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
            'referer' : '' }
cmd = 'wget --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0"  --directory-prefix=' + outdir + ' '

for i, x in enumerate(imgurls):
    #outfname = outdir + '/' + str(i) + '.' + url.split('.')[-1]
    #data = requests.get(url,headers=headers).text
    #print x[0]
    #cmdf = cmd + x[0] + ' --referer=' + x[1]
    #os.system(cmdf)
    headers['referer'] = x[1]
    resp = requests.get(x[0], headers=headers)
    with open( os.path.join(outdir, str(i) + '.' + x[0].split('.')[-1] ) , 'wb' ) as outfile:
        outfile.write(resp.content)
    print x[0]
"""
