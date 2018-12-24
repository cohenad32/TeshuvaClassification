#!/usr/bin/python3

from sklearn import datasets, svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, Perceptron

import numpy as np

from sklearn.pipeline import Pipeline

from sklearn.model_selection import GridSearchCV, train_test_split

print ("loading")

resp = datasets.load_files('testclassifier/', encoding='utf-8')

train_data, eval_data, train_target, eval_target = train_test_split(resp.data, resp.target, test_size=0.1)

print ("transform")
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=2, norm=None,
    encoding='utf-8', ngram_range=(1, 1), token_pattern=r'''(?u)\b\w[\w'"]+\b''', max_features=50000
    )

vtrain_data = tfidf.fit_transform(train_data)
print('fit_transform complete')
vtest_data = tfidf.transform(eval_data)

print ("tuning")

clf = SGDClassifier(penalty='elasticnet')
clf.fit(vtrain_data, train_target)

print('fitted, scoring:')

x = clf.score(vtrain_data, train_target)
y = clf.score(vtest_data, eval_target)

print (x, y)
print ("done")