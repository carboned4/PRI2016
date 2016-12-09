import nltk
import string
from nltk.corpus import stopwords
from nltk.collocations import *
import numpy

punct = string.punctuation
punct = punct.translate(None,"'")
exclude = set(punct)
stop = set(stopwords.words('english'))

def test_set(s):
    return ''.join(ch for ch in s if ch not in exclude)


#separacao em frases
etd = open('englishtextualdoc.txt')
etdread = etd.read()
etdread = etdread.decode('utf-8')
etdsentences = nltk.sent_tokenize(etdread)

sentenceslists = []
alltermsset = set()
for etdsentence in etdsentences:
    sentenceset = set()
    #limpeza de palavras
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
    #criacao de bigramas e trigramas
    docbigrams = list()
    doctrigrams = list()
    for iword in range(len(sentenceclean)):
        if iword < len(sentenceclean)-1:
            bigram = sentenceclean[iword] + " " + sentenceclean[iword+1]
            docbigrams += [bigram]
            if iword < len(sentenceclean)-2:
                trigram = sentenceclean[iword] + " " + sentenceclean[iword+1] + " " + sentenceclean[iword+2]
                doctrigrams += [trigram]
    #set com todos os termos de uma frase, depois colocados numa lista de frases
    sentenceset = sentenceset.union(set(docbigrams).union(set(doctrigrams)))
    sentenceslists += [list(sentenceset)]
    alltermsset = alltermsset.union(sentenceset)

alltermslist = list(alltermsset)
#iteracoes de PR armazenadas numa lista
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

#criacao do indice de termos e da iteracao 0 do PR
graphmatrix = list()
termindexes = dict()
for iterm in range(len(alltermslist)):
    termindexes[alltermslist[iterm]] = iterm;
    graphmatrix += [dict()]
    pagerankiterations[0] += [przero]
sortediterations[0] = sortIteration(0)


#preenchimento da matriz esparsa com ligacoes entre termos
for isentence in sentenceslists:
    for iterm in range(len(isentence)-1):
        for iterm2 in range(iterm+1,len(isentence)):
            term1 = termindexes[isentence[iterm]]
            term2 = termindexes[isentence[iterm2]]
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
            

#iteracoes de pagerank 1 a 50
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
