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
    #only read the first 2 documents (still very slow)
    if docreadindex == 5:
        break


print "calcular tfidf"
vectorizer2 = TfidfVectorizer( use_idf=True, tokenizer=my_tokenizer, smooth_idf=True)
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
    sumpjs = 0
    #prior(pi) = tfidf(pi) (feito acima)
    # sum weight(.,.) calculado abaixo, em sumlinkweights, para cada pj.
    # sum prior(.) calculado abaixo, em sumlinkpriors, para cada pi.
    # damper x tfidf(pi)/sumlinkpriors(pi) + (1-d) *
    # * sum[ pr(pj*weight(pj,pi)/sumlinkweights(pj) ]
    tfidfpi = docstfidf[idoc,vectorizer2.vocabulary_[alltermslist[ilink]]]
    sumlinkpriorspi = sumlinkpriors[pi]
    if sumlinkpriorspi == 0:
        return 0
    for pjlinkofpi in graphmatrix[pi].keys():
        parcel = pagerankiterations[lastPRiteration][pjlinkofpi]
        parcel *= sumlinkweights[pi]
        parcel = parcel/sumlinkweights[pjlinkofpi]
        sumpjs += parcel
    return damper * tfidfpi / sumlinkpriorspi +(1-damper)*sumpjs

def checkOrderIsDifferent(ii):
    sortdifferent = False
    for iterm in range(len(sortediterations[ii])):
        if sortediterations[ii][iterm] != sortediterations[ii-1][iterm]:
            sortdifferent = True
            break
    return sortdifferent


doccandidateslist = dict()

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
    przero = 1/bigN
    lastPRiteration = 0
    
    graphmatrix = list()
    termindexes = dict()
    sumlinkweights = dict()
    
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
                try:
                    graphmatrix[term1][term2] += 1
                    graphmatrix[term2][term1] += 1
                except Exception:
                    graphmatrix[term1][term2] = 1
                    graphmatrix[term2][term1] = 1
                try:
                    sumlinkweights[term1] +=1
                    sumlinkweights[term2] +=1
                except Exception:
                    sumlinkweights[term1] =1
                    sumlinkweights[term2] =1
    
    sumlinkpriors = dict()
    i = 0
    for iterm in graphmatrix:
        totalprior = 0
        for ilink in iterm.keys():
            totalprior+= docstfidf[idoc,vectorizer2.vocabulary_[alltermslist[ilink]]]
        sumlinkpriors[i] = totalprior
        i+=1
    #print sumlinkpriors
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
        #top5ranked += [(alltermslist[itop],pagerankiterations[lastPRiteration][itop])]
        top5ranked += [alltermslist[itop]]
    
    docname = docindexnames[idoc]
    doccandidateslist[docname] = top5ranked


#print doccandidateslist
#print top5rankedfordocs

#ficheiros das equipas
path = "fao30/indexers/iic1/"
keysfordoc = dict()
indexerIterator = 1
setForKeys = set()
for filename in os.listdir(path):
    while indexerIterator <= 6:
        etd = open(path + filename)
        etdread = etd.read()
        etdread = etdread.decode('latin-1')
        etd_keys = etdread.split("\n",-1)[:-1]
        fname = filename[:-4] + '.txt'
         
        setForKeys = setForKeys.union(set(etd_keys))
        
        etd_keys = list(setForKeys)
        keysfordoc[fname] = etd_keys
        indexerIterator += 1
        path = path[:-2] + str(indexerIterator) + "/"
    path = "fao30/indexers/iic1/"
    indexerIterator = 1




docAPs = dict()
#calculate AP and therefore MAP
aptotalsum = 0
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
    apitersum = 0
    for term in range(len(doccandidateslist[docname])):
        listansweri += [doccandidateslist[docname][term]]
        setanseri = set(listansweri)
        p = (len(setanseri.intersection(setrelevant)))/(len(setanseri)+0.0)
        r = int()
        if doccandidateslist[docname][term] in keysfordoc[docname]:
            r = 1
        else:
            r = 0
        apitersum += (p * r)
    ap = apitersum  / (sizeRel+0.0)
    docAPs[docname] = ap
    aptotalsum += ap
    listanswer = []
    setansweri = set()

        
print "map: " + str(aptotalsum/len(docindexnames))