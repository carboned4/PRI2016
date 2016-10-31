import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
import numpy

    
def sort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array


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

"""
####################
candidatesfordocs = dict()
for i in docindexnames:
    candidatesfordocs[docindexnames[i]] = dict()
for i in docindexnames:
    docname = docindexnames[i]
    print "doc "+str(i)+" "+docname
    for iword in range(len(vectorizer2.get_feature_names())):
        wordindoctfidf = docstfidf.getrow(i).toarray()[0][iword]
        if wordindoctfidf != 0:
            candidatesfordocs[docname][vectorizer2.get_feature_names()[iword]] = wordindoctfidf
"""

doccandidateslist = dict()
featurenames = list(vectorizer2.get_feature_names())
for idoc in range(len(docindexnames)):
    docname = docindexnames[idoc]
    featurenamescopy = numpy.array(featurenames)
    tfidfdoccopy = numpy.array(docstfidf.getrow(idoc).toarray()[0])
    sortedindices = (tfidfdoccopy.argsort()[-5:])[::-1]
    candidatewordsfordoc = list()
    for candidatei in sortedindices:
        candidatewordsfordoc += [featurenamescopy[candidatei]]
    doccandidateslist[docname] = candidatewordsfordoc
    print docname
    print candidatewordsfordoc
    
    
    
#sorted1 = sort(docstfidf.getrow(0).toarray()[0])[-5:]
#sorted1 = sorted1[::-1]



#print v
#print vectorizer2.idf_
"""
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