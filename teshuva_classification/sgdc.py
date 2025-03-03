import numpy
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, Perceptron, LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

print ("loading")

print ("loading")
import os
inputpath = 'testclassifier/'
outputpath = 'responsa'

classnames = []
for dirpath, dirnames, filenames in os.walk(inputpath):
    structure = os.path.join(outputpath, dirpath[len(inputpath):])
    classnames.append(dirnames)
    if not os.path.isdir(structure):
        os.mkdir(structure)

print(classnames)
classnames = classnames[0]
classnames.sort()
resp = datasets.load_files('testclassifier/', encoding='utf-8')

train_data, eval_data, train_target, eval_target = train_test_split(resp.data, resp.target, test_size=0.1)
print ("transform")
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm=None,
    encoding='utf-16', ngram_range=(1, 2), token_pattern=r'''(?u)\b\w[\w'"]+\b''', max_features=50000
    )

vtrain_data = tfidf.fit_transform(train_data)
vtrain_data = vtrain_data.todense()
print('fit_transform complete')
vtest_data = tfidf.transform(eval_data)
vtest_data = vtest_data.todense()

print ("tuning")

# loop through vtrain_data.data and vtest_data.data and create a new nd array with other things append. In order to add things to the vector, loop through train data
# and extract features from that and then add it to the corresponding vtrain_data.data

# import citation bag of words
f = open("../CRFSample-master/citationBagOfWords", encoding='utf-8').readlines()
bagOfWords = []
for word in f:
    word = word.strip("\n")
    bagOfWords.append(word)

bow = set()
from nltk import ngrams
for phrase in bagOfWords:
    phrase = phrase.replace(')', ') ')
    phrase = phrase.split()
    for i in range(1, len(phrase)+1):
        for n in ngrams(phrase, i):
            bow.add(' '.join(n))

print(len(bow), bow)
bagOfWords = list(bow)

# loop through the data and create a vector for the bag of words
# keep track of which vector corresponds to which bit of data

# adding to the train vectors
new_vtrain_data = []
dataNum = 0
rows, cols = vtrain_data.shape
for row in range(rows):
    for entry in vtrain_data[row]:
        sent = train_data[dataNum]
        sent = sent.split(" ")
        bagVector = numpy.zeros(len(bagOfWords), dtype=object)
        for i, w in enumerate(bagOfWords):
            if w in sent:
                bagVector[i] += 1
        # for word in words:
        #     for i, w in enumerate(bagOfWords):
        #         if word == w:
        #             bagVector[i] += 1
        #vtrain_data[row].data = numpy.append(vtrain_data[row].data, bagVector)
        new_vtrain_data.append(numpy.append(vtrain_data[row].data, bagVector)) # take the bag of words vector and add it back to the tfidf vector
        dataNum += 1
new_vtrain_data = numpy.asarray(new_vtrain_data)

# adding to the test vectors
new_vtest_data = []
dataNum = 0
rows, cols = vtest_data.shape
for row in range(rows):
    for entry in vtest_data[row]:
        sent = eval_data[dataNum]
        sent  = sent.split(" ")
        bagVector = numpy.zeros(len(bagOfWords), dtype=object)
        for i, w in enumerate(bagOfWords):
            if w in sent:
                bagVector[i] += 1
        #vtest_data[row].data = numpy.append(vtest_data[row].data, bagVector)
        new_vtest_data.append(numpy.append(vtest_data[row].data, bagVector)) # add the bag of words vector to the tfidf vector
        dataNum += 1
new_vtest_data = numpy.asarray(new_vtest_data)

# TODO: create a function that will transform all new data into vectors that include the bag of words
# TODO: change the vectors being used in x and y to be the new vectors that include BoW

clf = SGDClassifier(penalty='elasticnet')
#clf = MultinomialNB()
#clf = LogisticRegression()
clf.fit(new_vtrain_data, train_target)

print('fitted, scoring:')

x = clf.score(new_vtrain_data, train_target)
y = clf.score(new_vtest_data, eval_target)

print (x, y)
print ("done")


test_responsa = datasets.load_files('responsa/', encoding='utf-8')
test_responsa_data = test_responsa.data
test_responsa_target = test_responsa.target
test_responsa_data2 = tfidf.transform(test_responsa_data)
test_responsa_data2 = test_responsa_data2.todense()

# adding vectors to the test responsa - i.e continued transformation of the data
new_test_responsa_data = []
dataNum = 0
rows, cols = test_responsa_data2.shape
for row in range(rows):
    for entry in test_responsa_data2[row]:
        # entry = numpy.array(entry)
        # print(entry.shape)
        sent = test_responsa_data[dataNum]
        sent = sent.split(" ")
        bagVector = numpy.zeros(len(bagOfWords))
        for i, w in enumerate(bagOfWords):
            if w in sent:
                bagVector[i] += 1
        # test_responsa_data2[row].data = numpy.append(test_responsa_data2[row].data, bagVector)
        new_test_responsa_data.append(numpy.append(test_responsa_data2[row].data, bagVector))
        dataNum += 1

new_test_responsa_data = numpy.asarray(new_test_responsa_data)
y = clf.score(new_test_responsa_data, test_responsa_target)
print(y)
#
# n = 3
# probs = clf.predict_proba(new_test_responsa_data)
# best_n = numpy.argsort(probs, axis=1)[:,-n:]
#
# for responsum, guess, answer in zip(test_responsa.data, best_n, test_responsa_target):
#     print(responsum)
#     print(classnames[answer])
#     print(classnames[guess[0]], classnames[guess[1]], classnames[guess[2]])

test = clf.predict(new_test_responsa_data)
print(test)

for responsum, guess, answer in zip(test_responsa.data, test, test_responsa_target):
    print(responsum)
    print(classnames[guess], classnames[answer])