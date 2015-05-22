import glob
import sys
import os
import re
import numpy as np
import pdb
import pylab as pl
from random import shuffle
files = glob.glob( 'parsed/*' )
ctext = []
stopwords = [ 'he', 'she', 'it', 'for', 'if', 'is', 'the', 'was',
              'were', 'that', 'there', 'this', 'then', 'him', 'her',
              'them', 'us', 'are', 'of', 'and', 'who', 'how', 'what',
              'when', 'an', 'as','his', 'have', 'had', 'by', 'not',
              'in'  ]
patt = '\"|\,|\;|\:|\;|\?|\(|\)|\[|\]|\*|\!|\'|\<|\>|\{|\}|\n|\t|\.'
total_tokens = []
shuffle(files)
for fname in files[:30]:
    data = open(fname).read()
    data = re.sub( patt, ' ', data )
    data = re.sub(' [a-zA-Z] ',' ',data)
    data = data.lower()
    tokens = data.split()
    cleaned = [ tk for tk in tokens if tk not in stopwords ]
    cleaned = [ tk for tk in cleaned if tk[0] != '#' ]
    cleaned = [ tk for tk in cleaned if len(re.findall('[0-9]+',tk)) == 0 ]
    total_tokens += cleaned
    ctext.append( cleaned )

utokens = list( set(total_tokens) )
wmap = dict([ ( x, i) for i,x in enumerate(utokens) ])

matrix = np.zeros(( len(utokens), len(utokens) ) )

"""
for i, token in enumerate(utokens):
    for j, doc in enumerate(ctext):
        matrix[i][j] += doc.count(token)
"""

wsize = 3
for cblock in ctext:
    for i in range(0, len(cblock)):
        cword = cblock[i]
        start = i - wsize
        if i - wsize < 0:
            start = 0
        for token in cblock[start:i+wsize]:
            matrix[wmap[cword]][wmap[token]] += 1

print matrix.shape
print utokens[100:200]
#pdb.set_trace()
U, s, V = np.linalg.svd(matrix)
#indices = [ 188,4567,14482,9259,4344,5363,3746,15853,6775,7664, 8236, 5064,13981,1644, 8355 ]
txts = [ 'delhi', 'kejriwal', 'panneerselvam', 'jayalalithaa' ,'arvind', 'aap', 'china', 'korea', 'iaf', 'yamuna', 'fighter', 'gadkari', 'cag', 'nepal', 'sushil', 'modi' ]
indicesmap = {}
for txt in txts:
    try:
        indx = utokens.index(txt)
        indicesmap[txt] = indx
    except:
        continue
x = []
y = []
for txt in indicesmap.keys():
    x.append(U[indicesmap[txt],1])
    y.append(U[indicesmap[txt],2])

pl.plot(x, y,'go')
for txt in indicesmap.keys():
    pl.annotate(txt, (U[indicesmap[txt],1],U[indicesmap[txt],2]))
pl.show()
    
#pdb.set_trace()
