from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib, requests
import re, sys, os
import wget

def fetch(url):
    return urllib.urlopen(url).read()

def create_parser(url):
    data = fetch(url)
    soup = BeautifulSoup(data,'lxml')
    return soup

def parse_seasons_page(url):
    soup = create_parser(url)
    return [ x.findAll('a')[0]['href'] for x in soup.findAll('h2','lists') ]

def parse_seasons_listings(url):
    soup = create_parser(url)
    return map( lambda x : 'http://watch-series-tv.to' + x, \
                [ x['content'] for x in soup.findAll('meta',{'itemprop':'url'}) ] )

def parse_episode_page(url):
    soup = create_parser(url)
    gorillavids = [x['href'] for x in soup.findAll('a',{'title':'gorillavid.in'}) ]
    return 'http://watch-series-tv.to' + gorillavids[0]

def get_gorillavid_page(url):
    display = Display(visible=0, size=(800, 600))
    display.start()
    path_to_chromedriver = './chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    browser = webdriver.Chrome()
    browser.get(url)
    pgsource = browser.page_source
    soup = BeautifulSoup(pgsource,'lxml')
    browser.quit()
    display.stop()
    return soup.findAll('a','push_button blue')[0]['href']
    
def get_gorillavid_postp(url):
    while True:
        soup = create_parser(url)
        params = [ 'op','usr_login','id','fname','referer','channel','method_free' ]
        post_params = {}
        try:
            for param in params:
                x = soup.findAll('input',{'type':'hidden','name': param } )[0]['value']
                post_params[param] = x
            break
        except:
            continue
    return post_params

def get_gorillavid_video(url,ref):
    payload = get_gorillavid_postp(url)
    payload['referer'] = ref
    video_reg = 'http\:\/\/[0-9\.\:]+\/[a-z0-9]+\/video\.[0-9a-z]{3}'
    r = requests.post( url, data=payload )
    return (re.findall(video_reg,r.text)[0],payload['fname'])

def check_chromedriver():
    filepath = 'http://chromedriver.storage.googleapis.com/2.20/chromedriver_linux64.zip'
    if not os.path.exists( 'chromedriver' ):
        os.system( 'wget ' + filepath )
        os.system( 'unzip *.zip' )

if __name__ == '__main__':
    check_chromedriver()
    series_page = sys.argv[1]
    season = int(sys.argv[2]) - 1
    episodes_range = (int(sys.argv[3].split('-')[0])-1,int(sys.argv[3].split('-')[1]))
    seasons = parse_seasons_page(series_page)
    seasons.reverse()
    episodes = parse_seasons_listings(seasons[season])
    episodes.reverse()
    for episode in episodes[episodes_range[0]:episodes_range[1]]:
        episode_source = parse_episode_page(episode)
        print episode_source
        gorilla_page = get_gorillavid_page(episode_source)
        print '\nGetting video url ...'
        video,fname = get_gorillavid_video(gorilla_page,episode_source)
        if os.path.exists( fname ):
            print '\nDownloaded ', fname
            continue
        print '\nDowloading ', fname
        wget.download(video, out=fname)
