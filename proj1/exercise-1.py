import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.collocations import *
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
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
etdwords = list()
for etdsentence in etdsentences:
    sentencenopunct = test_set(etdsentence.lower())
    sentencewords = nltk.word_tokenize(sentencenopunct)
    for i in range(len(sentencewords)):
        word = sentencewords[i]
        if word[0] == "'":
            word = word[1:]
        sentencewords[i] = word
    sentenceclean = [i for i in sentencewords if i not in stop]
    etdwords += sentenceclean
etdbigrams = list(nltk.bigrams(etdwords))
#print etdbigrams
candidates = list()
candidates += etdwords
for bi in etdbigrams:
    candidates += [bi[0]+" "+bi[1]]
    

train = fetch_20newsgroups(subset='train')
englishdocplustrain = train.data + candidates
test = fetch_20newsgroups(subset='test')
vectorizer2 = TfidfVectorizer( use_idf=True, ngram_range=(1,2))
trainvec2 = vectorizer2.fit_transform(englishdocplustrain)








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