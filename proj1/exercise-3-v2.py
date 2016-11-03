import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
import operator
import re

numberofdocuments = 0
totalwordsperdocument = dict()

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
        print candidate
        if isinstance(candidate, tuple):
            candidate = " ".join(candidate)
            print "was tuple"
        print candidate
        candidatetags = nltk.pos_tag(nltk.word_tokenize(candidate))
        for taggedterm in candidatetags:
            stringtocheck += "<"+taggedterm[1]+">"
        parseResult = regexparser2.match(stringtocheck)
        if parseResult:
            newCandidates += [candidate]
    return newCandidates

# http://stackoverflow.com/questions/3994493/checking-whole-string-with-a-regex

punct = string.punctuation
punct = punct.translate(None,"'")
punctexcludeset = set(punct)
stop = set(stopwords.words('english'))
def test_set(s):
    return ''.join(ch for ch in s if ch not in punctexcludeset)
def my_tokenizer(documentasstring):
    docsentences = nltk.sent_tokenize(documentasstring)
    docwords = list()
    for docsentence in docsentences:
        sentencenopunct = test_set(docsentence.lower())
        sentencewords = nltk.word_tokenize(sentencenopunct)
        for i in range(len(sentencewords)):
            word = sentencewords[i]
            if word[0] == "'":
                word = word[1:]
            sentencewords[i] = word
        sentenceclean = [i for i in sentencewords if i not in stop]
        docwords += sentenceclean
    #all the words are split
    print docwords
    docbigrams = list(nltk.bigrams(docwords))
    doctrigrams = list(nltk.trigrams(docwords))
    docterms = docwords + docbigrams + doctrigrams
    print docterms
    docvalidterms = filterCandidates(docterms)
    return docvalidterms


countVectorizer = CountVectorizer(tokenizer=my_tokenizer)
countVectorizer.build_analyzer()
docstf = countVectorizer.fit_transform(set([("Alice stopped by the big big station to retrieve the blue poop")]))
vecvocab = countVectorizer.vocabulary_

