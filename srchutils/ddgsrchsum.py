import mechanicalsoup
import sys
import time
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import argparse

lang = "english"
sent = 5

parser = argparse.ArgumentParser(description='duckduckgo search and summarizer')
parser.add_argument('-q', action="store", default='', dest='q')
parser.add_argument('-n', action="store", default=10, dest='n', type=int)
parser.add_argument('-l', action="store", default=5, dest='l', type=int)

def summarize(url):
    summary = []
    parser = HtmlParser.from_url(url,Tokenizer(lang))
    stemmer = Stemmer(lang)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(lang)
    for sentence in summarizer(parser.document,sent):
        summary.append(sentence._text)
    return ' '.join(summary)

if __name__ == '__main__':
    results = parser.parse_args()
    srchterm = results.q
    sent = results.l
    noofsrchs = results.n
    if srchterm == '':
        print 'No search query'
        sys.exit(0)
        
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://duckduckgo.com/")
    browser.select_form('#search_form_homepage')
    browser["q"] = srchterm
    browser.submit_selected()

    count = 0
    for link in browser.get_current_page().select('a.result__a'):
        srchtext = link.text
        srchurl = link.attrs['href']
        try:
            summary = summarize(srchurl)
            print '-'*80
            print srchtext + '\n'
            print srchurl + '\n'
            print summary
            print '-'*80 + '\n'
        except Exception as e:
            print '-'*80
            print srchtext + '\n'
            print srchurl + '\n'
            print '-'*80 + '\n'
        count += 1
        if count > noofsrchs:
            break
