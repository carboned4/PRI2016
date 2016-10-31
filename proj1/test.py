import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator

import os
path = "fao30/documents/"

all_docs = []
for filename in os.listdir(path):
    print filename
    etd = open(path + filename)
    etdread = etd.read()
    etdread = etdread.decode('latin-1')
    etd_words = nltk.word_tokenize(etdread)
    all_docs += [etdread]

stop = set(stopwords.words('english'))

vectorizer2 = TfidfVectorizer( use_idf=True, ngram_range=(1,2), stop_words=stop )
v = vectorizer2.fit_transform(all_docs)
vec3vocab = vectorizer2.vocabulary_
print v
print vectorizer2.idf_
