import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
import re


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