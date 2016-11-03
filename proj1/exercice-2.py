import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import f1_score

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
indexerIterator = 1
setForKeys = set()
while indexerIterator <= 6:
    for filename in os.listdir(path):
        etd = open(path + filename)
        etdread = etd.read()
        etdread = etdread.decode('latin-1')
        etd_keys = etdread.split("\n",-1)[:-1]
        filename = filename[:-4] + '.txt'
         
        setForKeys = setForKeys.union(set(etd_keys))
        
        #sera muito estupido o que estou a fazer????
        etd_keys = list(setForKeys)
        keysfordoc[filename] = etd_keys

        
    indexerIterator += 1
    path = path[:-2] + str(indexerIterator) + "/"


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
    #print docname
    #print candidatewordsfordoc
    

    

measuresdoc = dict()
for idoc in range(len(docindexnames)):
    measures= dict()
    docname = docindexnames[idoc]
    setrelevant = set(keysfordoc[docname])
    setanswer = set(doccandidateslist[docname])
    sizeRel = len(setrelevant)
    sizeAns = len(setanswer)
    sizeInt = len(setrelevant.intersection(setanswer))
    pr = sizeInt/(0.0+sizeAns)
    re = sizeInt/(0.0+sizeRel)
    try:
        f1 = (2*re*pr)/(re+pr)
    except ZeroDivisionError:
        f1 = 0

    measures["pr"] = pr
    measures["re"] = re
    measures["f1"] = f1
    measuresdoc[docname] = measures

ap = 0
apdict = dict()
for idoc in range(len(docindexnames)):
    docname = docindexnames[idoc]
    setrelevant = set(keysfordoc[docname])
    setanswer = set(doccandidateslist[docname])
    sizeRel = len(setrelevant)
    sizeAns = len(setanswer)
    sizeInt = len(setrelevant.intersection(setanswer))
    pr = sizeInt/(0.0+sizeAns)
    re = sizeInt/(0.0+sizeRel)
    listansweri = []
    setansweri = set()
    ap=dict()
    apsum = 0
    for term in range(len(doccandidateslist[docname])):
        listansweri += [doccandidateslist[docname][term]]
        setanseri = set(listansweri)
        p = (len(setanseri.intersection(setrelevant)))/(len(setanseri)+0.0)
        r = int()
        if doccandidateslist[docname][term] in keysfordoc[docname]:
            r = 1
        else:
            #print docname
            r = 0
        ap[term+1] = (p * r) / (sizeRel+0.0)
        apsum +=  (p * r) / (sizeRel+0.0)
    apdict[docname] = ap
    measuresdoc[docname]["map"] = apsum/(0.0+len(doccandidateslist[docname]))
    ap = 0
    listanswer = []
    setansweri = set()

        
        