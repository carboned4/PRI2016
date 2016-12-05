import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
import numpy

punct = string.punctuation
punct = punct.translate(None,"'")
exclude = set(punct)
stop = set(stopwords.words('english'))

def test_set(s):
    return ''.join(ch for ch in s if ch not in exclude)


#exercise 1 - part 1 - reading words
#english textual document
etd = open('englishtextualdoc.txt')
etdread = etd.read()
etdread = etdread.decode('utf-8')
etdsentences = nltk.sent_tokenize(etdread)

sentenceslists = []
alltermsset = set()
for etdsentence in etdsentences:
    sentenceset = set()
    
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
    
    sentenceset = set(sentenceclean)
    
    docbigrams = list()
    doctrigrams = list()
    for iword in range(len(sentenceclean)):
        if iword < len(sentenceclean)-1:
            bigram = sentenceclean[iword] + " " + sentenceclean[iword+1]
            docbigrams += [bigram]
            if iword < len(sentenceclean)-2:
                trigram = sentenceclean[iword] + " " + sentenceclean[iword+1] + " " + sentenceclean[iword+2]
                doctrigrams += [trigram]
    sentenceset = sentenceset.union(set(docbigrams).union(set(doctrigrams)))
    sentenceslists += [list(sentenceset)]
    alltermsset = alltermsset.union(sentenceset)

alltermslist = list(alltermsset)
pagerankiterations = list()
pagerankiterations += [[]]
sortediterations = list()
sortediterations += [[]]
bigN = len(alltermslist)
przero = 1.0/bigN
lastPRiteration = 0


def sortIteration(it):
    iterationcopy = numpy.array(pagerankiterations[it])
    sortedindices = (iterationcopy.argsort())[::-1]
    return sortedindices


graphmatrix = list()
termindexes = dict()
for iterm in range(len(alltermslist)):
    termindexes[alltermslist[iterm]] = iterm;
    graphmatrix += [dict()]
    pagerankiterations[0] += [przero]
sortediterations[0] = sortIteration(0)



for isentence in sentenceslists:
    for iterm in range(len(isentence)-1):
        for iterm2 in range(iterm+1,len(isentence)):
            term1 = termindexes[isentence[iterm]]
            term2 = termindexes[isentence[iterm2]]
            #print str(len(isentence)) + " " +str(term1) + " " + str(term2)
            graphmatrix[term1][term2] = 1
            graphmatrix[term2][term1] = 1



damper = 0.15
def pageranki(pi):
    sum = 0
    for pjLinkOfpi in graphmatrix[pi].keys():
        sum += pagerankiterations[lastPRiteration][pjLinkOfpi]/(len(graphmatrix[pjLinkOfpi]))
    return damper/bigN+(1-damper)*sum

def checkOrderIsDifferent(ii):
    sortdifferent = False
    for iterm in range(len(sortediterations[ii])):
        if sortediterations[ii][iterm] != sortediterations[ii-1][iterm]:
            sortdifferent = True
            break
    return sortdifferent
            


for iterationi in range(1,51):
    pagerankiterations += [list()]
    for pi in range(len(alltermslist)):
        pagerankiterations[iterationi] += [pageranki(pi)]
    sortediterations += [sortIteration(iterationi)]
    orderisdifferent = checkOrderIsDifferent(iterationi)
    lastPRiteration = iterationi
    if orderisdifferent != True:
        break



top5indices = sortediterations[lastPRiteration][:5]
top5ranked = list()
for itop in top5indices:
    top5ranked += [(alltermslist[itop],pagerankiterations[lastPRiteration][itop])]


print "\n" + str(lastPRiteration) + " iterations"
print "term , pagerank"
print top5ranked
