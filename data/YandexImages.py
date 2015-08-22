from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
from urllib2 import unquote
import json
import pdb

srchurl = 'https://www.yandex.com/images/search?text=%s'

class YandexImages():
    def __init__( self ):
        #self.display = Display(visible=0, size=(800, 600))
        #self.display.start()
        self.base_url = srchurl
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.buton = '/html/body/div[4]/div[2]/div/div[3]/a'

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry) )
        self.browser.get(url)
        clicked = 0
        for i in range(1,20):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i* 10000))
            #pdb.set_trace()
            try:
                cleme = self.browser.find_element_by_link_text('More images')
                cleme.click()
            except:
                pass
            #pdb.set_trace()
            time.sleep(4)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'div' )
        imgs = [ y for y in x if 'serp-item' in y['class'] ]
        print len(x)
        #pdb.set_trace()
        print imgs[0]
        jsimgs = [ json.loads(img['data-bem']) for img in imgs ]
        realimgs = [ x['serp-item']['fullscreen'][0]['url'] for x in jsimgs ]
        return realimgs

    def stop():
        browser.quit()
        display.stop()

if __name__ == '__main__':
    gimgs = YandexImages()
    urls =  gimgs.crawl(sys.argv[1:])
    with open( '_'.join(sys.argv[1:]) , 'w' ) as outfile:
        for x in urls:
            outfile.write( x + '\n' )

