import nltk
import string
from nltk.corpus import stopwords
from nltk.collocations import *
import numpy
import lxml.etree as etree
from yattag import Doc
import math
import os



etdsentences = list()
doc = etree.parse('http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml')
for item in doc.xpath('/rss/channel/item'):
    restitle = item.find('title').text
    resdescription = item.find('description').text
    etdsentences += [restitle]
    etdsentences += [resdescription]
    #restitle.encode('cp850', errors='replace')
    #resdescription.encode('cp850', errors='replace')


punct = string.punctuation
punct = punct.translate(None,"'")
exclude = set(punct)
stop = set(stopwords.words('english'))

def test_set(s):
    return ''.join(ch for ch in s if ch not in exclude)


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



topindices = sortediterations[lastPRiteration][:100]
topranked = list()
for itop in topindices:
    topranked += [alltermslist[itop]]

#http://stackoverflow.com/questions/6748559/generating-html-documents-in-python
#http://www.yattag.org/
doc, tag, text = Doc().tagtext()
with tag('html'):
    with tag('header'):
        with tag('style'):
            text('p { margin: 0px; text-align: center; font-family: Helvetica;}')
            text('h1 { margin: 5px; text-align: center; font-size: 60px; font-family: Helvetica;}')
            text('h2 { margin: 5px; text-align: center; font-size: 40px; font-family: Helvetica;}')
    with tag('body'):
        with tag('h1'):
            text('RSS: Technology')
        with tag('h2'):
            text('Group 4')
        for icandidate in range(len(topranked)):
            fontsize = int(20.0 + 30.0 / math.sqrt(icandidate+1))
            fontcolor = " hsl(220, "+str(int(100.0 - 100.0 * (icandidate/100.0)))+"%, 40%)"
            print fontcolor
            with tag('p'):
                with tag('span', style = 'font-size:'+str(fontsize)+'px; color: ' + fontcolor + ";", title= str(icandidate+1)):
                    text(topranked[icandidate])

result = doc.getvalue()
os.remove("tech.html")
f = open('tech.html', 'w')
f.write(result.encode('ascii', 'xmlcharrefreplace'))
f.close()