import os,sys
from bs4 import BeautifulSoup
import glob
from json import JSONEncoder

def parsefile(fname):
    data = open(fname).read()
    soup = BeautifulSoup(data,'lxml')
    reviews = soup.findAll('div', 'fclear fk-review fk-position-relative line ' )
    extReviews = []
    for review in reviews:
        rating = review.findAll('div','fk-stars')[0]['title']
        title = review.findAll('div','line fk-font-normal bmargin5 dark-gray')[0].text
        text = review.findAll('span','review-text')[0].text
        content = { 'title' : title,
                    'text' : text,
                    'rating' : rating }
        extReviews.append(content)
    return extReviews


files = glob.glob( sys.argv[1] + '/*.html' )
reviews = []
for fname in files:
     reviews += parsefile(fname)
     print 'Done ..', fname
with open( 'reviewparsed.tsv', 'w' ) as outfile:
    for review in reviews:
        outfile.write( JSONEncoder().encode(review) + '\n' )
