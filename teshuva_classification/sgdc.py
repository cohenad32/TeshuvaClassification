import numpy
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

print ("loading")

resp = datasets.load_files('testclassifier/', encoding='utf-8')

train_data, eval_data, train_target, eval_target = train_test_split(resp.data, resp.target, test_size=0.1)

print ("transform")
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm=None,
    encoding='utf-16', ngram_range=(1, 2), token_pattern=r'''(?u)\b\w[\w'"]+\b''', max_features=50000
    )

vtrain_data = tfidf.fit_transform(train_data)
print('fit_transform complete')
vtest_data = tfidf.transform(eval_data)

print ("tuning")

# loop through vtrain_data.data and vtest_data.data and create a new nd array with other things append. In order to add things to the vector, loop through train data
# and extract features from that and then add it to the corresponding vtrain_data.data

# import citation bag of words
f = open("/Users/adinacohen/Documents/GitHub/TeshuvaClassification/CRFSample-master/citationBagOfWords").readlines()
bagOfWords = []
for word in f:
    word = word.strip("\n")
    bagOfWords.append(word)

# loop through the data and create a vector for the bag of words
# keep track of which vector corresponds to which bit of data
dataNum = 0
rows, cols = vtrain_data.shape
for row in range(rows):
    for entry in vtrain_data[row]:
        # entry = numpy.array(entry)
        # print(entry.shape)
        sent = train_data[dataNum]
        words = sent.split(" ")
        bagVector = numpy.zeros(len(bagOfWords))
        for word in words:
            for i, w in enumerate(bagOfWords):
                if word == w:
                    bagVector[i] += 1
        entry = numpy.append(entry, bagVector, axis=50000)
        # print(entry.shape)
        dataNum += 1

# for file in train_data:
#     for sent in file:
#         sent = sent.strip.split()
#         bagVector = numpy.zeros(len(bagOfWords))
#         for word in sent:
#             for i, w in enumerate(bagOfWords):
#                 if word == w:
#                     bagVector[i] += 1


clf = MultinomialNB()
clf.fit(vtrain_data, train_target)

print('fitted, scoring:')

x = clf.score(vtrain_data, train_target)
y = clf.score(vtest_data, eval_target)

print (x, y)
print ("done")


test_responsa = datasets.load_files('responsa/', encoding='utf-8')
test_responsa_data = test_responsa.data
test_responsa_target = test_responsa.target
test_responsa_data = tfidf.transform(test_responsa_data)
y = clf.score(test_responsa_data, test_responsa_target)
print(y)

test = clf.predict(test_responsa_data)
print(test)

