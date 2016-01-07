# -*- coding: utf-8 -*-

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import data_sets

#train = data_sets.en_train
#test = data_sets.en_test
train = data_sets.subte_train
test = data_sets.subte_test

#tx_cl = "I feel amazing!"
#tx_prob = "This one's a doozy."
tx_cl = "El subte esta demorado"
tx_prob = "El subte funciona bien"

cl = NaiveBayesClassifier(train)
print cl.classify(tx_cl)
print cl.classify("El subte funciona bien")
prob_dist = cl.prob_classify(tx_prob)
print prob_dist.max()
print round(prob_dist.prob("pos"), 2)
print round(prob_dist.prob("neg"), 2)

print cl.accuracy(data_sets.en_test)
print cl.show_informative_features(5)

#Using TextBlob
blob = TextBlob("No funca por que hay obras para mejorar la cosa", classifier=cl)
print blob.sentiment
print blob.classify()

blob = TextBlob("El subte funciona normal", classifier=cl)
print blob.sentiment
print blob.classify()

blob = TextBlob("Se realizan obras en el subte A", classifier=cl)
print blob.sentiment
print blob.classify()

blob = TextBlob("No funciona, anda averiguar por que. Quizas hay un accidente", classifier=cl)
print blob.sentiment
print blob.classify()

blob = TextBlob(u"El subte funciona ok", classifier=cl)
print blob.sentiment
print blob.classify()