import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
import operator

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
    for i in range(len(sentencewords)):
        word = sentencewords[i]
        if word[0] == "'":
            word = word[1:]
        if word != "":
            sentencewords[i] = word
    sentenceclean = [i for i in sentencewords if i not in stop]
    
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
bigN = len(sentenceslists)
previousPRiteration = 0
print pagerankiterations
print str(len(pagerankiterations))

graphmatrix = list()
termindexes = dict()
for iterm in range(len(alltermslist)):
    termindexes[alltermslist[iterm]] = iterm;
    graphmatrix += [dict()]
    pagerankiterations[0]+=[1.0/bigN]

print "sentencesets"
"""
sentencesets
aqui já criou uma lista de termos (uni, bi, tri) para cada frase, sem repetições.
também já criou o mapeamento termo-índice e a matriz do garfo.
depois, iterar em triângulo para criar a matriz do grafo.
"""

for isentence in sentenceslists:
    for iterm in range(len(isentence)-1):
        for iterm2 in range(iterm+1,len(isentence)):
            term1 = termindexes[isentence[iterm]]
            term2 = termindexes[isentence[iterm2]]
            #print str(len(isentence)) + " " +str(term1) + " " + str(term2)
            graphmatrix[term1][term2] = 1
            graphmatrix[term2][term1] = 1

"""
^ ao invés daquele truque de iterar em triângulo, podia tentar-se isto:
http://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
"""
damper = 0.15
def pageranki(pi):
    sum = 0
    for pjlinkofpi in graphmatrix[pi].keys():
        sum += pagerankiterations[previousPRiteration][pjlinkofpi]/(len(graphmatrix[pjlinkofpi]))
    return damper/bigN+(1-damper)*sum

for iterationi in range(1,51):
    pagerankiterations += [list()]
    for pi in range(len(alltermslist)):
        pagerankiterations[iterationi] += [pageranki(pi)]
    # MISSING - check if order is still the same
    previousPRiteration = iterationi


globalwords = {}
DFdict = {}

def processDoc(docwords, name):
    f1counts = {}
    for word in docwords:
        if word in f1counts.keys():
            f1counts[word]+=1
        else:
            f1counts[word] = 1
    
    for word in f1counts.keys():
        if word in globalwords.keys():
            globalwords[word][name] = f1counts[word]
        else:
            globalwords[word] = {}
            globalwords[word][name] = f1counts[word]
    return


processDoc(candidates, "Alice")
vec3vocab = vectorizer2.vocabulary_
idfdict = {}
for term in candidates:
    try:
        idfdict[term] = vectorizer2.idf_[vec3vocab[term]] * globalwords[term]['Alice']
    except Exception:
        pass

sorted_x = sorted(idfdict.items(), key=operator.itemgetter(1))
for i in range(5):
    print sorted_x[i]