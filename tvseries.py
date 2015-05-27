from bs4 import BeautifulSoup
import urllib
import requests
import re

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
    soup = create_parser(url)
    return soup.findAll('a','push_button blue')[0]['href']
    
def get_gorillavid_postp(url):
    soup = create_parser(url)
    params = [ 'op','usr_login','id','fname','referer','channel','method_free' ]
    post_params = {}
    for param in params:
        x = soup.findAll('input',{'type':'hidden','name': param } )[0]['value']
        post_params[param] = x
    return post_params

def get_gorillavid_video(url,ref):
    payload = get_gorillavid_postp(url)
    payload['referer'] = ref
    video_reg = 'http\:\/\/[0-9\.\:]+\/[a-z0-9]+\/video\.[0-9a-z]{3}'
    r = requests.post( url, data=payload )
    return re.findall(video_reg,r.text)[0]

if __name__ == '__main__':
    seasons = parse_seasons_page('http://watch-series-tv.to/serie/modern_family')
    episodes = parse_seasons_listings(seasons[3])
    for episode in episodes:
        episode_source = parse_episode_page(episode)
        gorilla_page = get_gorillavid_page(episode_source)
        print episode
        print gorilla_page
        print get_gorillavid_video(gorilla_page,episode_source)
