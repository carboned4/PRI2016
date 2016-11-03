import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
import re


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
        candidatetags = nltk.pos_tag(nltk.word_tokenize(candidate))
        for taggedterm in candidatetags:
            stringtocheck += taggedterm[1]
        parseResult = regexparser2.match(stringtocheck)
        if parseResult:
            newCandidates += [candidate]
            print "yay"
        newCandidates = newCandidates[:-1]
        """parseTree = regexparser.parse(candidatetags)
        #cases: (success/fail)
        # (S aaa/NN...
        # (S (NP aaa/NN...
        # 0123
        if len(parseTree) == 1:
            # good candidate!
            newCandidates += [candidate]
        # else not a candidate"""
        
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
    docvalidwords = filterCandidates(docwords)
    docvalidbigrams = list(nltk.bigrams(docvalidwords))
    docvalidtrigrams = list(nltk.trigrams(docvalidwords))
    docvalidterms = docvalidwords + docvalidbigrams + docvalidtrigrams
    return docvalidterms