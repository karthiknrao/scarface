from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
from urllib2 import unquote
import pdb

srchurl = 'https://www.flickr.com/search/?text=%s'

class BaiduImages():
    def __init__( self ):
        #self.display = Display(visible=0, size=(800, 600))
        #self.display.start()
        self.srchurl = 'https://www.flickr.com/search/?text=%s'
        self.base_url = srchurl
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.buton = '//*[@id="yui_3_5_1_1_1440135195051_1805"]'

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry)  )
        self.browser.get(url)
        clicked = 0
        for i in range(1,20):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i* 10000))
            #pdb.set_trace()
            try:
                click = self.browser.find_element_by_class_name('alt')
                click.click()
                print 'Hi'
            except:
                pass
            time.sleep(11)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'div', 'view photo-list-photo-view awake' )
        print len(x)
        pdb.set_trace()
        print x[0]
        imgs = [ y['style'].split('url')[1].replace(')','').replace(';','').replace('(','') for y in x ]
        def zimage(url):
            if '_m.jpg' in url:
                return url.replace( '_m', '_z' )
            elif '_n.jpg' in url:
                return url.replace( '_n', '_z' )
            else:
                return url.replace( '.jpg', '_z.jpg' )
        return [ zimage(x) for x in imgs ]

    def stop():
        browser.quit()
        display.stop()

if __name__ == '__main__':
    gimgs = BaiduImages()
    urls =  gimgs.crawl(sys.argv[1:])
    with open( '_'.join(sys.argv[1:]) , 'w' ) as outfile:
        for x in urls:
            outfile.write( x + '\n' )
