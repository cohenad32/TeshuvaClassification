#!/usr/bin/python3

from sklearn import datasets, svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, Perceptron

import numpy as np

from sklearn.pipeline import Pipeline

from sklearn.model_selection import GridSearchCV, train_test_split

print ("loading")

resp = datasets.load_files('testclassifier/', encoding='utf-16')

train_data, eval_data, train_target, eval_target = train_test_split(resp.data, resp.target, test_size=0.1)

print ("transform")
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm=None,
    encoding='utf-16', ngram_range=(1, 2), token_pattern=r'''(?u)\b\w[\w'"]+\b''', max_features=50000
    )

vtrain_data = tfidf.fit_transform(train_data)
print('fit_transform complete')
vtest_data = tfidf.transform(eval_data)

print ("tuning")

# clf = SGDClassifier(penalty='elasticnet')
clf = MultinomialNB()
clf.fit(vtrain_data, train_target)

print('fitted, scoring:')

x = clf.score(vtrain_data, train_target)
y = clf.score(vtest_data, eval_target)

print (x, y)
print ("done")


test_responsa = datasets.load_files('responsa/', encoding='utf-16')
test_responsa_fit = tfidf.fit_transform(test_responsa)
clf.fit(test_responsa_fit, train_target)

test = clf.predict(test_responsa_fit)