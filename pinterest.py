from selenium import webdriver
import sys
import os
import time
from bs4 import BeautifulSoup

path_to_chromedriver = 'chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# do login 
browser.get( 'https://in.pinterest.com/login/' )
elem = browser.find_elements_by_name("username_or_email")
elem[0].send_keys("karthik.n.rao0110@gmail.com")
elem = browser.find_elements_by_name("password")
elem[0].send_keys("qawsedrf")
elem = browser.find_elements_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/form/div[4]/div/button")
elem[0].click()


def noImages(psource):
    if psource == None:
        return 0
    soup = BeautifulSoup(psource,'lxml')
    imgs = soup.findAll('div','Image Module pinUiImage')
    return len(imgs)
    
# do search
url = 'https://in.pinterest.com/search/pins/?q=scarlett+johansson'
#url = 'https://in.pinterest.com/kgage83/shoes/'
browser.get(url)
time.sleep(1)

pps = None
cps = None
for i in range(1,30):
    browser.execute_script("window.scrollTo(0, %d);" % ( i * 10000))
    time.sleep(20)
    cps = browser.page_source
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
    extractedUrls.append( url + '\t' + title )

with open( 'pinterestcrawl.tsv', 'w' ) as outfile:
    outfile.write( '\n'.join(extractedUrls) )
