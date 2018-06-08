#encoding=utf-8

# Copyright (c) 2017 Deyatech. All rights reserved.
# Authors: Peter Podstreleny <peter.podstreleny@deyatech.com>

# classify.py

# This script performs Naive Bayes classification.
# https://en.wikipedia.org/wiki/Naive_Bayes_classifier

import os
import json
from decimal import *

user = 'admin'
import_path = 'C:/Users/wangy/PycharmProjects/hw/peter/target/output/'

def conditionalDocumentProbability(document, contract):
    # https://en.wikipedia.org/wiki/Conditional_probability
    # Returns conditional document probability p(D|A)
    # Given the category 'contract', what is the probability of document
    # Given the category 'non-contract', what is the probability of document
    # p(D|A) = p(W1|A) * p(W2|A) * ... * p(WN|A)
    # p(D|~A) = p(W1|~A) * p(W2|~A * ... * p(WN|~A))


    # Problems with multiplying very small fractional numbers:

    # Probability multiplication in Python only works correctly until approximatelly
    # e-320 (320 places after decimal point). After this, the system experiences
    # floating point underflow as the number is too small and it is rounded to 0.
    # This causes problems with probability multiplication with 0.

    # Common solution to this is to transfer the probability multiplication into
    # logarithmic space. Python library Decimal makes this easier to handle. Here
    # are some links for more details:

    # https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html
    # https://docs.python.org/3/library/decimal.html
    # https://stackoverflow.com/questions/3704570/in-python-small-floats-tending-to-zero

    # Setup context for fractional precision (in this case e-1000)
    getcontext().prec = 1000

    result = Decimal(1.0)
    for word in document:
        result = result * Decimal(conditionalWordProbability(word, contract))
    return result

def conditionalWordProbability(word, contract):
    # https://en.wikipedia.org/wiki/Additive_smoothing
    # https://stats.stackexchange.com/questions/256409/naive-bayes-with-laplace-smoothing-probabilities-not-adding-up?rq=1
    # 'alpha' represents Laplace smoothing. Laplace smoothing is used to cover
    # edge case when words in document being classified don't exist in the
    # training data set. This fixes issues with 0 probabilities & therefore
    # incorrect classification.

    # This returns conditional probability p(W|A) with smoothing
    # Given the category 'contract', what is the probability of word (with smoothing)
    # Given the category 'non-contract' what is the probability of word (with smoothing)

    alpha = 1

    if contract:
        # print('-----')
        # print((model['trainPositive'].get(word, 0) + alpha) / (float(model['totalPositive'] + (alpha * model['totalAllUnique']))))
        return ((model['trainPositive'].get(word, 0) + alpha) / (float(model['totalPositive'] + (alpha * model['totalAllUnique']))))
    else:
        # print('-----')
        # print((model['trainNegative'].get(word, 0) + alpha) / (float(model['totalNegative'] + (alpha * model['totalAllUnique']))))
        return ((model['trainNegative'].get(word, 0) + alpha) / (float(model['totalNegative'] + (alpha * model['totalAllUnique']))))

def classify(document):
    isContract = Decimal(model['p(A)']) * conditionalDocumentProbability(document, True)         # P(A|D)
    isNotContract = Decimal(model['p(~A)']) * conditionalDocumentProbability(document, False)    # p(~A|D)
    print('------------------------------------------------------------------')
    if (isContract > isNotContract):
        print('Document is CONTRACT')
    else:
        print('Document is NOT CONTRACT')
    print('------------------------------------------------------------------')
    print('CONTRACT probability:      ' + str(isContract/(isContract + isNotContract)*100) + '%')
    print('NOT CONTRACT probability: ' + str(isNotContract/(isContract + isNotContract)*100) + '%')
    print('------------------------------------------------------------------')
    print('p(A|D): ' + str(isContract))
    print('p(~A|D): ' + str(isNotContract))
    print('------------------------------------------------------------------')

# Open & load model
with open('model.txt', 'r') as file:
    model = json.load(file)

# Load document to classify
import_path = unicode(import_path, "utf8")
for filename in os.listdir(import_path):
    print('-------------------------------------------------------------------')
    print('--- File: ' + filename)
    print('... opening ...')
    print('... classifying ...')
    name = os.path.join(import_path, filename)
    print('... filename ...',name)

    with open(name, 'r', encoding="utf8") as f1:
        content = json.load(f1)

# Classify document
classify(content['body'])
