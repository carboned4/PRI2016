import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
import operator
import re
from math import log10
import numpy


#general statistics that we'll calculate further down
numberofdocuments = 0
totalwordsperdocument = dict()
totalwordsincorpus = 0


#checking if a term (uni/bi/trigram) matches a regex.
#conversao passo-a-passo da gramatica do enunciado
#grammar2 = r'(<NN[A-Z]*>)+$'
#grammar2 = r'(<JJ> <NN[A-Z]*>)+$'
#grammar2 = r'((<JJ>)* <NN[A-Z]*>)+$'
#grammar2 = r'((<IN>)?(<JJ>)*<NN[A-Z]*>)+$'
#grammar2 = r'((<IN>)?(<JJ>)*(<NN[A-Z]*>)+)+$'
grammar2 = r'(((<JJ>)*(<NN[A-Z]*>)+<IN>)?(<JJ>)*(<NN[A-Z]*>)+)+$'
regexparser2 = re.compile(grammar2)
def filterCandidates(candidatesList):
    newCandidates = []
    for candidate in candidatesList:
        stringtocheck = ""
        if isinstance(candidate, tuple):
            candidate = " ".join(candidate)
        candidatetags = nltk.pos_tag(nltk.word_tokenize(candidate))
        for taggedterm in candidatetags:
            stringtocheck += "<"+taggedterm[1]+">"
        parseResult = regexparser2.match(stringtocheck)
        if parseResult:
            newCandidates += [candidate]
    return newCandidates


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
    docwords = list()
    doclength = 0
    for docsentence in docsentences:
        sentencenopunct = test_set(docsentence.lower())
        sentencewords = nltk.word_tokenize(sentencenopunct)
        doclength += len(sentencewords)
        for i in range(len(sentencewords)):
            word = sentencewords[i]
            if word[0] == "'":
                word = word[1:]
            sentencewords[i] = word
        sentenceclean = [i for i in sentencewords if i not in stop]
        docwords += sentenceclean
    totalwordsperdocument[docindex] = doclength
    totalwordsincorpus += doclength
    #all the words are split
    docbigrams = list(nltk.bigrams(docwords))
    doctrigrams = list(nltk.trigrams(docwords))
    docterms = docwords + docbigrams + doctrigrams
    docvalidterms = filterCandidates(docterms)
    docindex +=1
    numberofdocuments +=1
    return docvalidterms

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



#uses a vectorizer to calculate term frequency
countVectorizer = CountVectorizer(tokenizer=my_tokenizer)
countVectorizer.build_analyzer()
#docstf = countVectorizer.fit_transform(set(["Alice stopped by the big big station to retrieve the blue poop","Alice stopped by a poop and was angry"]))
docstf = countVectorizer.fit_transform(all_docs)
vecvocab = countVectorizer.vocabulary_



#calculates the IDF according to the new formula
idfDict = dict()
for termi in range(len(vecvocab)):
    docswithterm = docstf.getcol(termi).getnnz(0)[0]
    numerator = numberofdocuments - docswithterm +0.5
    denominator = docswithterm +0.5
    idfDict[termi] = log10(numerator/denominator)


#calculates the BM25 for a term,document
k1 = 1.2
b = 0.75
def score(documentn, termi):
    idfpart = idfDict[termi]
    ftD = docstf[documentn,termi]
    avgdl = totalwordsincorpus/(0.0+numberofdocuments)
    #print ftD
    numeratorpart = ftD * (k1 + 1)
    denominatorpart = ftD + k1 * (1 - b + b * (totalwordsperdocument[documentn]/avgdl) )
    scoredt = idfpart * (numeratorpart / denominatorpart)
    return scoredt


#all the scores will be calculated here
dictscores = dict()
for doci in range(numberofdocuments):
    documentscores = dict()
    for termi in range(len(vecvocab)):
        documentscores[termi] = score(doci, termi)
    dictscores[doci] = documentscores


doccandidateslist = dict()
featurenames = list(countVectorizer.get_feature_names())
featurenamescopy = numpy.array(featurenames)
for idoc in range(numberofdocuments):
    bm25doccopy = numpy.array(dictscores[idoc].values())
    #the keys were inserted by order, so the values were by this order as well
    sortedindices = (bm25doccopy.argsort()[-5:])[::-1]
    candidatewordsfordoc = list()
    for candidatei in sortedindices:
        candidatewordsfordoc += [featurenamescopy[candidatei]]
    doccandidateslist[idoc] = candidatewordsfordoc
    #print docname
    #print candidatewordsfordoc
    
