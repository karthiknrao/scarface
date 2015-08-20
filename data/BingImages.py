#from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
import pdb

class BingImages():
    def __init__( self ):
        #self.display = Display(visible=0, size=(800, 600))
        #self.display.start()
        self.base_url = 'https://www.bing.com/images/search?q=%s'
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.buton = '//*[@id="b_content"]/div[7]/a'

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry) )
        self.browser.get(url)
        clicked = 0
        for i in range(1,12):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i* 10000))
            but = self.browser.find_elements_by_xpath(self.buton)
            if len(but) != 0 and clicked == 0:
                clicked = 1
                but[0].click()
            time.sleep(4)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'img' )
        print len(x)
        imgs = [ y['src'].split('&')[0] for y in x if 'mm.bing.net/th?id=' in y['src'] ]
        
        return imgs

    def stop():
        browser.quit()
        display.stop()

if __name__ == '__main__':
    gimgs = BingImages()
    urls =  gimgs.crawl(sys.argv[1:])
    with open( '_'.join(sys.argv[1:]) , 'w' ) as outfile:
        for x in urls:
            outfile.write( x + '\n' )
