import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator

import os
path = "C:\PRI2016\proj1/testes/"

all_docs = []
for filename in os.listdir(path):
    etd = open(path + filename)
    etdread = etd.read()
    etdread = etdread.decode('utf-8')
    #print '++++++++++++++++++++\n'
    etd_words = nltk.word_tokenize(etdread)
    #print etd_words
    all_docs += etd_words
   # print '++++++++++++++++++++\n'
 #   print 'shit'


vectorizer2 = TfidfVectorizer( use_idf=False )
vectorizer2.fit_transform(all_docs)
vec3vocab = vectorizer2.vocabulary_
print vec3vocab
