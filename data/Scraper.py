from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time, os, sys
import requests
from urllib2 import unquote
import pdb

class BaiduImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(1200, 800))
        self.display.start()
        self.srchurl = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%s&oq=%s&rsp=-1'
        self.base_url = self.srchurl
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.buton = '//*[@id="yui_3_5_1_1_1440135195051_1805"]'

    def crawl(self, qry ):
        url = self.base_url % ( '+'.join(qry), '+'.join(qry)  )
        self.browser.get(url)
        clicked = 0
        for i in range(1,20):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i* 10000))
            #pdb.set_trace()
            click = self.browser.find_element_by_id('pageMore')
            print 'Hi'
            try:
                click.click()
            except:
                pass
            time.sleep(2)
        pages = self.browser.page_source
        soup = BeautifulSoup(pages,'lxml')
        x = soup.findAll( 'li', 'imgitem' )
        print len(x)
        #pdb.set_trace()
        print x[0]
        realimgs = [ unquote(y.findAll('a')[0]['href'].split('objurl=')[1]) for y in x ]
        baiduimgs = [ y.findAll('img','main_img img-hover')[0]['src'] for y in x ]
        imgs = zip(baiduimgs, realimgs)
        
        final =  [ '\t'.join(x) for x in imgs ]
        with open( '_'.join(sys.argv[1:]) + '_Baidu' , 'w' ) as outfile:
            for x in final:
                outfile.write( x + '\n' )

    def stop(self):
        self.browser.quit()
        self.display.stop()

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
        final =  [ '\t'.join(x) for x in imgurls ]
    
        with open( '_'.join(sys.argv[1:]) + '_Google' , 'w' ) as outfile:
            for x in final:
                outfile.write( x + '\n' )


    def stop(self):
        self.browser.quit()
        self.display.stop()


class BingImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
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
        
        with open( '_'.join(sys.argv[1:]) + '_Bing' , 'w' ) as outfile:
            for x in imgs:
                outfile.write( x + '\n' )

        #return imgs

    def stop(self):
        self.browser.quit()
        self.display.stop()

class YahooImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.srchurl = 'https://in.images.search.yahoo.com/search/images;_ylt=A2oKiHNJt9ZVZXYAtRe9HAx.;_ylu=X3oDMTBsZ29xY3ZzBHNlYwNzZWFyY2gEc2xrA2J1dHRvbg--;_ylc=X1MDMjExNDcyMzAwNQRfcgMyBGJjawNhbzM1NDIxYTVnbGVoJTI2YiUzRDMlMjZzJTNEZ2cEZnIDc2ZwBGdwcmlkAwRtdGVzdGlkA251bGwEbl9zdWdnAzAEb3JpZ2luA2luLmltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzUEcXVlcnkDc2hvZXMEdF9zdG1wAzE0NDAxMzUxOTUEdnRlc3RpZANudWxs?pvid=bMbV3zEwNi6sDKQQVFhV0QkCMTExLgAAAACOPtRY&p=%s&fr=sfp&fr2=sb-top-in.images.search.yahoo.com&ei=UTF-8&n=60&x=wrt&y=Search'
        self.base_url = self.srchurl
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
            try:
                but.click()
            except:
                pass
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
        
        with open( '_'.join(sys.argv[1:]) + '_Yahoo' , 'w' ) as outfile:
            for x in imgs:
                outfile.write( x + '\n' )

        #return imgs

    def stop(self):
        self.browser.quit()
        self.display.stop()

class FlickrImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.srchurl = 'https://www.flickr.com/search/?text=%s'
        self.base_url = self.srchurl
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
        final =  [ zimage(x) for x in imgs ]
        with open( '_'.join(sys.argv[1:]) + '_Flickr', 'w' ) as outfile:
            for x in final:
                outfile.write( x + '\n' )


    def stop(self):
        self.browser.quit()
        self.display.stop()

class PinterestImages():
    def __init__( self ):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.srchurl = 'https://in.pinterest.com/search/pins/?q=%s'
        self.base_url = self.srchurl
        self.path_to_chromedriver = './chromedriver'
        self.browser = webdriver.Chrome(executable_path = self.path_to_chromedriver)
        self.browser = webdriver.Chrome()
        self.browser.get( 'https://in.pinterest.com/login/' )
        self.elem = self.browser.find_elements_by_name("username_or_email")
        self.elem[0].send_keys("karthik.n.rao0110@gmail.com")
        self.elem = self.browser.find_elements_by_name("password")
        self.elem[0].send_keys("qawsedrf")
        self.elem = self.browser.find_elements_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/form/div[4]/div/button")
        self.elem[0].click()

        self.buton = '//*[@id="yui_3_5_1_1_1440135195051_1805"]'

    def crawl(self, qry ):
        def noImages(psource):
            if psource == None:
                return 0
            soup = BeautifulSoup(psource,'lxml')
            imgs = soup.findAll('div','Image Module pinUiImage')
            return len(imgs)

        url = self.base_url % ( '+'.join(qry)  )
        self.browser.get(url)
        time.sleep(1)
        pps = None
        cps = None
        for i in range(1,20):
            self.browser.execute_script("window.scrollTo(0, %d);" % ( i * 10000))
            time.sleep(10)
            cps = self.browser.page_source
            if noImages(cps) < noImages(pps):
                break
            pps = cps

        pagesource = pps

        soup = BeautifulSoup(pagesource,'lxml')
        imgs = soup.findAll('div','Image Module pinUiImage')
        extractedUrls = []
        for img in imgs:
            imgd = img.findAll('img')
            url = imgd[0]['src']
            title = imgd[0]['alt'].encode( 'ascii', 'ignore')
            extractedUrls.append( url.replace('236x','736x') + '\t' + title )

        with open( '_'.join(sys.argv[1:]) + '_Pinterest', 'w' ) as outfile:
            for x in extractedUrls:
                outfile.write( x + '\n' )


    def stop(self):
        self.browser.quit()
        self.display.stop()


if __name__ == '__main__':

    print 'Baidu..'
    gimgs = BaiduImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()

    print 'Google..'
    gimgs = GoogleImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()

    print 'Yahoo..'
    gimgs = YahooImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()

    print 'Bing..'
    gimgs = BingImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()

    print 'Flickr..'
    gimgs = FlickrImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()

    print 'Pinterest..'
    gimgs = PinterestImages()
    gimgs.crawl(sys.argv[1:])
    gimgs.stop()
