from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
import pdb

srchurl = 'https://in.images.search.yahoo.com/search/images;_ylt=A2oKiHNJt9ZVZXYAtRe9HAx.;_ylu=X3oDMTBsZ29xY3ZzBHNlYwNzZWFyY2gEc2xrA2J1dHRvbg--;_ylc=X1MDMjExNDcyMzAwNQRfcgMyBGJjawNhbzM1NDIxYTVnbGVoJTI2YiUzRDMlMjZzJTNEZ2cEZnIDc2ZwBGdwcmlkAwRtdGVzdGlkA251bGwEbl9zdWdnAzAEb3JpZ2luA2luLmltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzUEcXVlcnkDc2hvZXMEdF9zdG1wAzE0NDAxMzUxOTUEdnRlc3RpZANudWxs?pvid=bMbV3zEwNi6sDKQQVFhV0QkCMTExLgAAAACOPtRY&p=%s&fr=sfp&fr2=sb-top-in.images.search.yahoo.com&ei=UTF-8&n=60&x=wrt&y=Search'
buttons = [ '//*[@id="yui_3_5_1_1_1440135195051_1805"]', ]
class YahooImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.base_url = srchurl
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.buton = '//*[@id="yui_3_5_1_1_1440135195051_1805"]'

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry) )
        self.browser.get(url)
        clicked = 0
        for i in range(1,12):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i* 10000))
            but = self.browser.find_element_by_class_name('more-res')
            #pdb.set_trace()
            #if len(but) != 0 and clicked == 0:
            #    but[0].click()
            but.click()
            time.sleep(4)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'img', {'alt':''} )
        print len(x)
        #pdb.set_trace()
        imgs = []
        for y in x:
            try:
                imgs.append(y['src'])
            except:
                imgs.append(y['data-src'])
                pass
        
        return imgs

    def stop():
        browser.quit()
        display.stop()

if __name__ == '__main__':
    gimgs = YahooImages()
    urls =  gimgs.crawl(sys.argv[1:])
    with open( '_'.join(sys.argv[1:]) , 'w' ) as outfile:
        for x in urls:
            outfile.write( x + '\n' )
