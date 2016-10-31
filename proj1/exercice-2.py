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
docindexnames = dict()
docindex = 0
for filename in os.listdir(path):
    docindexnames[docindex] = filename
    etd = open(path + filename)
    etdread = etd.read()
    etdread = etdread.decode('latin-1')
    etd_words = nltk.word_tokenize(etdread)
    all_docs += [etdread]
    docindex += 1

stop = set(stopwords.words('english'))

vectorizer2 = TfidfVectorizer( use_idf=True, ngram_range=(1,2), stop_words=stop )
docstfidf = vectorizer2.fit_transform(all_docs)
vecvocab = vectorizer2.vocabulary_

####################

path = "fao30/indexers/iic1/"

keysfordoc = dict()
for filename in os.listdir(path):
    etd = open(path + filename)
    etdread = etd.read()
    etdread = etdread.decode('latin-1')
    etd_keys = etdread.split("\n",-1)[:-1]
    keysfordoc[filename] = etd_keys


####################
"""

"""


for docname in docindexnames.keys():
    


#print v
#print vectorizer2.idf_

candidates = list()

globalwords = {}
DFdict = {}

def processDoc(docwords, name):
    f1counts = {}
    for word in docwords:
        if word in f1counts.keys():
            f1counts[word]+=1
        else:
            f1counts[word] = 1
    
    for word in f1counts.keys():
        if word in globalwords.keys():
            globalwords[word][name] = f1counts[word]
        else:
            globalwords[word] = {}
            globalwords[word][name] = f1counts[word]
    return


"""
processDoc(candidates, "Alice")
vec3vocab = vectorizer2.vocabulary_
idfdict = {}
for term in candidates:
    try:
        idfdict[term] = vectorizer2.idf_[vec3vocab[term]] * globalwords[term]['Alice']
    except Exception:
        pass

sorted_x = sorted(idfdict.items(), key=operator.itemgetter(1))
for i in range(5):
    print sorted_x[i]
"""