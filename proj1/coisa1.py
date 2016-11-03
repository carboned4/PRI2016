import codecs
import operator
import math

globalwords = {}
docNames = []
DFdict = {}
IDFdict = {}

def processoDoc(name):
    f1counts = {}
    f1words = list()
    f1 = codecs.open(name, mode='r', encoding='utf-8')
    f1read = f1.read()
    f1.close()
    docNames.append(name)
    f1lines = f1read.split("\n",-1)
    for el in f1lines:
        f1words = f1words + el.split(" ",-1)
    for word in f1words:
        if word in f1counts.keys():
            f1counts[word.encode('utf-8')]+=1
        else:
            f1counts[word.encode('utf-8')] = 1
    
    for word in f1counts.keys():
        if word in globalwords.keys():
            globalwords[word][name] = f1counts[word]
        else:
            globalwords[word] = {}
            globalwords[word][name] = f1counts[word]
    return

def countAll():
    total = 0
    for worddict in globalwords.values():
        for value in worddict.values():
            total += value
    return total

def DF():
    DFdict.clear()
    for word in globalwords.keys():
        DFdict[word] = len(globalwords[word].keys())
    return DFdict

def maxminTerm():
    sorted_x = sorted(DFdict.items(), key=operator.itemgetter(1))
    return [sorted_x[0][1],sorted_x[-1][1]]

def IDF():
    IDFdict.clear()
    for word in DFdict.keys():
        IDFdict[word] = math.log(float(len(docNames))/DFdict[word])
    return IDFdict

def dotproduct(query):
    similarities = {}
    idfcalc = IDF()
    query = query.split(" ",-1)
    for term in query:
        for doc in globalwords[term]:
            if doc not in similarities.keys():
                similarities[doc] = 0
            similarities[doc]+= globalwords[term][doc]*idfcalc[term]
    return similarities

def stats():
    print("number of docs\n ", len(docNames))
    print("number of terms\n ", countAll())
    print("number of individual terms\n ", len(globalwords.keys()))
    print("DF", DF())
    print("max",maxminTerm()[1],"min",maxminTerm()[0])
    print("IDF",IDF())
    return

processoDoc("f1.txt")
processoDoc("f2.txt")
processoDoc("f3.txt")
stats()
print dotproduct("input")