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
totaltermsincorpus = 0

#maximum number of words in an N-gram (approximation)
maxN = 3


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
    global maxN
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
    docbigrams = []
    doctrigrams = []
    for iword in range(len(docwords)):
        if maxN >= 2:
            if iword < len(docwords)-1:
                bigram = docwords[iword] + " " + docwords[iword+1]
                #print bigram
                docbigrams += [bigram]
                if maxN >= 3:
                    #print "enter max 3"            
                    if iword < len(docwords)-2:
                        trigram = docwords[iword] + " " + docwords[iword+1] + " " + docwords[iword+2]
                        doctrigrams += [trigram]
    docterms = docwords + docbigrams + doctrigrams
    totaltermsincorpus += len(docterms)
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



#uses a vectorizer to calculate term frequency
countVectorizer = CountVectorizer(tokenizer=my_tokenizer)
countVectorizer.build_analyzer()
#docstf = countVectorizer.fit_transform(set(["Alice stopped by the big big station to retrieve the blue poop","Alice stopped by a poop and was angry"]))
docstf = countVectorizer.fit_transform(all_docs)
vecvocab = countVectorizer.vocabulary_


"""
def read_text_in_dict(text):
    freq_dict = get_all_ngrams(text,3)
    total_term_count = 0
    for key in freq_dict:
        total_term_count += freq_dict[key]
    return freq_dict, total_term_count



def print_top_n_terms(score_dict,n):
    sorted_terms = sorted(score_dict.items(),key=operator.itemgetter(1),reverse=True)
    i=0
    for (term,score) in sorted_terms:
        i += 1
        print(term,score)
        if i==n:
            break
"""
#fg_dict, bg_dict = dict(),dict()
#fg_term_count, bg_term_count = 0,0
"""
print("Read foreground file",foreground_file)
with open(foreground_file,'r') as fg:
    fgtext=fg.read()
    fg_dict, fg_term_count = read_text_in_dict(fgtext)

print("Read background file",background_file)
with open(background_file,'r') as bg:
    bgtext=bg.read()
    bg_dict, bg_term_count = read_text_in_dict(bgtext)
"""

"""
kldiv_per_term = dict()
for term in fg_dict:
    fg_freq = fg_dict[term]

    # kldivI is kldiv for informativeness: relative to bg corpus freqs
    bg_freq = 1
    if term in bg_dict:
        bg_freq = bg_dict[term]
    relfreq_fg = float(fg_freq)/float(fg_term_count)
    relfreq_bg = float(bg_freq)/float(bg_term_count)

    kldivI = relfreq_fg*math.log(relfreq_fg/relfreq_bg)

    # kldivP is kldiv for phraseness: relative to unigram freqs
    unigrams = term.split(" ")
    relfreq_unigrams = 1.0
    for unigram in unigrams:
        if unigram in fg_dict:
            # stopwords are not in the dict
            u_freq = fg_dict[unigram]
            u_relfreq = float(u_freq)/float(fg_term_count)
            relfreq_unigrams *= u_relfreq
    kldivP = relfreq_fg*math.log(relfreq_fg/relfreq_unigrams)
    kldiv = kldivI+kldivP
    kldiv_per_term[term] = kldiv
    #print(term,kldivI,kldivP,kldiv)

print("\n\nTop terms:")
print_top_n_terms(kldiv_per_term,10)

"""

accumulatefreqDict = dict()
for termi in range(len(vecvocab)):
    acumforterm = docstf.getcol(termi).sum(0)[0]
    accumulatefreqDict[termi] = acumforterm



#calculates the phraseness for a term,document
def phraseness(documentn, termi):
    #pw = lmn bg - we use the approximation
    #qw = lm1 bg (unigram) - words are independent so we
    #just multiply their probabilities
    pw = float(accumulatefreqDict[termi])/float(totaltermsincorpus)    
    termunigrams = termi.split()
    qw = 1
    for uni in termunigrams:
        qw *= float(accumulatefreqDict[uni])/float(totalwordsincorpus)
    return pw*log10(pw/qw)


#calculates the informativeness for a term,document
def informativeness(documentn, termi):
    #pw = lm1 fg (unigram)
    #qw = lm1 bg (unigram)
    # words are independent so we just multiply their probabilities    
    termunigrams = termi.split()
    pw = 1
    for uni in termunigrams:
            pw *= float(docstf[documentn, uni])/float(totalwordsperdocument[documentn])
    qw = 1
    for uni in termunigrams:
        qw *= float(accumulatefreqDict[uni])/float(totalwordsincorpus)
    return pw*log10(pw/qw)


#all the scores will be calculated here
dictscores = dict()
for doci in range(numberofdocuments):
    documentscores = dict()
    for termi in range(len(vecvocab)):
        documentscores[termi] = informativeness(doci, termi) + phraseness(doci, termi)
    dictscores[doci] = documentscores


doccandidateslist = dict()
featurenames = list(countVectorizer.get_feature_names())
featurenamescopy = numpy.array(featurenames)
for idoc in range(numberofdocuments):
    probdoccopy = numpy.array(dictscores[idoc].values())
    #the keys were inserted by order, so the values were by this order as well
    sortedindices = (probdoccopy.argsort()[-5:])[::-1]
    candidatewordsfordoc = list()
    for candidatei in sortedindices:
        candidatewordsfordoc += [featurenamescopy[candidatei]]
    doccandidateslist[idoc] = candidatewordsfordoc
    