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
sentenceslistsfordocs = list()
#sentenceslists += [[]]
alltermssetfordoc = list()

def test_set(s):
    return ''.join(ch for ch in s if ch not in punctexcludeset)

def my_tokenizer(documentasstring):
    #these variables have to be declared here as global so the vectorizer can
    #see them from our program (we first declared them earlier)
    global docindex
    global totalwordsincorpus
    global numberofdocuments
    global alltermssetfordoc
    global sentenceslistsfordocs
    docterms = list()
    doclength = 0
    alltermssetforthisdoc = set()
    sentenceslistforthis = list()
    
    docsentences = nltk.sent_tokenize(documentasstring)
    print docindex
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
        sentencetermsset = set(sentenceterms)
        docterms += sentenceterms
        sentenceslistforthis += [sentenceterms]
        alltermssetforthisdoc = alltermssetforthisdoc.union(sentencetermsset)    
    #totalwordsperdocument[docindex] = len(alltermssetfordoc)
    #totalwordsincorpus += len(alltermssetfordoc)
    sentenceslistsfordocs += [sentenceslistforthis]
    alltermssetfordoc += [alltermssetforthisdoc]
    print "done " + str(docindex)
    docindex +=1
    numberofdocuments +=1
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
    if docreadindex == 3:
        break


print "calcular tfidf"
vectorizer2 = TfidfVectorizer( use_idf=True, tokenizer=my_tokenizer)
docstfidf = vectorizer2.fit_transform(all_docs)
vecvocab = vectorizer2.vocabulary_
print "calculado tfidf"

#---------------------
#funcoes para pagerank


def sortIteration(it):
    iterationcopy = numpy.array(pagerankiterations[it])
    sortedindices = (iterationcopy.argsort())[::-1]
    return sortedindices

damper = 0.15
def pageranki(pi):
    sum = 0
    for pjlinkofpi in graphmatrix[pi].keys():
        sum += pagerankiterations[lastPRiteration][pjlinkofpi]/(len(graphmatrix[pjlinkofpi]))
    return damper/bigN+(1-damper)*sum

def checkOrderIsDifferent(ii):
    sortdifferent = False
    for iterm in range(len(sortediterations[ii])):
        if sortediterations[ii][iterm] != sortediterations[ii-1][iterm]:
            sortdifferent = True
            break
    return sortdifferent


top5rankedfordocs = list()

print "calcular pagerank"
#calculo de pagerank
alltermslistfordocs = list()
for idoc in range(len(docindexnames)):
    print "pr "+str(idoc)
    alltermslist = list(alltermssetfordoc[idoc])
    pagerankiterations = list()
    pagerankiterations += [[]]
    sortediterations = list()
    sortediterations += [[]]
    bigN = len(alltermslist)
    przero = 1.0/bigN
    lastPRiteration = 0
    
    graphmatrix = list()
    termindexes = dict()
    for iterm in range(len(alltermslist)):
        termindexes[alltermslist[iterm]] = iterm;
        graphmatrix += [dict()]
        pagerankiterations[0] += [przero]
    sortediterations[0] = sortIteration(0)    

    for isentence in sentenceslistsfordocs[idoc]:
        for iterm in range(len(isentence)-1):
            for iterm2 in range(iterm+1,len(isentence)):
                term1 = termindexes[isentence[iterm]]
                term2 = termindexes[isentence[iterm2]]
                #print str(len(isentence)) + " " +str(term1) + " " + str(term2)
                graphmatrix[term1][term2] = 1
                graphmatrix[term2][term1] = 1
    
    for iterationi in range(1,51):
        pagerankiterations += [list()]
        for pi in range(len(alltermslist)):
            pagerankiterations[iterationi] += [pageranki(pi)]
        sortediterations += [sortIteration(iterationi)]
        orderisdifferent = checkOrderIsDifferent(iterationi)
        lastPRiteration = iterationi
        if orderisdifferent != True:
            break
    #done para este doc?
    top5indices = sortediterations[lastPRiteration][:5]
    top5ranked = list()
    for itop in top5indices:
        top5ranked += [(alltermslist[itop],pagerankiterations[lastPRiteration][itop])]
    
    top5rankedfordocs += [top5ranked]
    
"""
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
"""


#print doccandidateslist
print top5rankedfordocs
