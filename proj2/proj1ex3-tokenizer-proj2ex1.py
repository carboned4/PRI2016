import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
import re
from math import log10
import numpy


#general statistics that we'll calculate further down
numberofdocuments = 0
totalwordsperdocument = dict()
totalwordsincorpus = 0


#CUSTOM TOKENIZER
#this tokenizer will split words, delete stop words and punctuation and
#transform it into uni/bi/trigrams, which will all be filtered by the regex.
#some document and general statistics are also calculated here.
punct = string.punctuation
punct = punct.translate(None,"'")
punctexcludeset = set(punct)
stop = set(stopwords.words('english'))
docindex = 0

def test_set(s):
    return ''.join(ch for ch in s if ch not in punctexcludeset)

def my_tokenizer(documentasstring):
    #these variables have to be declared here as global so the vectorizer can
    #see them from our program (we first declared them earlier)
    global docindex
    global totalwordsincorpus
    global numberofdocuments
    docsentences = nltk.sent_tokenize(documentasstring)
    docterms = list()
    doclength = 0
    print docindex
    #alltermsset = set()
    #sentenceslists = []
    for etdsentence in docsentences:
        
        sentencenopunct = test_set(etdsentence.lower())
        sentencewords = nltk.word_tokenize(sentencenopunct)
        sentencewords2 = list()
        for i in range(len(sentencewords)):
            word = sentencewords[i]
            if word[0] == "'":
                word = word[1:]
            if word == "'":
                continue
            if word == "":
                continue
            sentencewords2 += [word]
        sentenceclean = [i for i in sentencewords2 if i not in stop]
        
        #sentenceterms = sentenceclean
        
        docbigrams = list()
        doctrigrams = list()
        for iword in range(len(sentenceclean)):
            if iword < len(sentenceclean)-1:
                bigram = sentenceclean[iword] + " " + sentenceclean[iword+1]
                docbigrams += [bigram]
                if iword < len(sentenceclean)-2:
                    trigram = sentenceclean[iword] + " " + sentenceclean[iword+1] + " " + sentenceclean[iword+2]
                    doctrigrams += [trigram]
        sentenceterms = sentenceclean + docbigrams + doctrigrams
        docterms += sentenceterms
        #sentenceslists += [sentenceterms]
        #alltermsset = alltermsset.union(set(sentenceterms))    
    #totalwordsperdocument[docindex] = len(alltermsset)
    #totalwordsincorpus += len(alltermsset)
    docindex +=1
    numberofdocuments +=1
    print "done " + str(docindex)
    return docterms

#PROCESSING:

#documents from FAO30 (same as exercise-2)

import os
path = "fao30/documents/"

all_docs = []
docindexnames = dict()
docreadindex = 0
for filename in os.listdir(path):
    docindexnames[docreadindex] = filename
    etd = open(path + filename)
    etdread = etd.read()
    etdread = etdread.decode('latin-1')
    etd_words = nltk.word_tokenize(etdread)
    all_docs += [etdread]
    docreadindex += 1


vectorizer2 = TfidfVectorizer( use_idf=True, tokenizer=my_tokenizer)
docstfidf = vectorizer2.fit_transform(all_docs)
vecvocab = vectorizer2.vocabulary_


#calculate tf-idf for each document
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
    
print doccandidateslist
