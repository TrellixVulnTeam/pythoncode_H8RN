#encoding=utf-8

# Copyright (c) 2017 Deyatech. All rights reserved.
# Authors: Peter Podstreleny <peter.podstreleny@deyatech.com>

# train.py

# This script calculates data needed for data model.

import os
import json

# Model structure
pContract = 0           # p(A)  - probability of contract
pNonContract = 0        # p(~A) - probability of non contract
trainPositive = {}      # dictionary of word frequency in contract documents
trainNegative = {}      # dictionary of word frequency in non contract documents
totalPositive = 0       # number of all words in contract documents
totalNegative = 0       # number of all words in non contract documents
totalAllUnique = set()  # number of all unique words in all documents (positive, negative)

# Helper functions
def train(training_data):
    totalContracts = 0
    totalDocuments = 0
    for document in training_data:
        if document['label'] == 'contract':
            totalContracts += 1
        totalDocuments += 1
        # Process document generates word frequency list
        processDocument(document['body'], document['label'])
    global pContract
    pContract = totalContracts / float(totalDocuments)
    global pNonContract
    pNonContract = (totalDocuments - totalContracts) / float(totalDocuments)

def processDocument(body, label):
    for word in body:
        if label == 'contract':
            trainPositive[word] = trainPositive.get(word, 0) + 1
            global totalPositive
            totalPositive = totalPositive + 1
        else:
            trainNegative[word] = trainNegative.get(word, 0) + 1
            global totalNegative
            totalNegative = totalNegative + 1
        global totalAllUnique
        totalAllUnique.add(word)

# Open data & load training data
with open('data.txt', 'r') as file:
    training_data = json.load(file)

# Train model
train(training_data)

# Build model
model = {
    'p(A)': pContract,
    'p(~A)': pNonContract,
    'trainPositive': trainPositive,
    'trainNegative': trainNegative,
    'totalPositive': totalPositive,
    'totalNegative': totalNegative,
    'totalAllUnique': len(totalAllUnique)
}

# Save model
with open('model.txt', 'w', encoding='utf8') as f2:
     f2.write(json.dumps(model))

# Save positive vocabulary
with open('positive-vocabulary.txt', 'w', encoding='utf8') as f3:
    for item in trainPositive:
        f3.write(item + os.linesep)

# Save negative vocabulary
with open('negative-vocabulary.txt', 'w', encoding='utf8') as f4:
    for item in trainNegative:
        f4.write(item + os.linesep)

print('-------------------------------------------------------------------')
print('--- Training is completed!')
print('-------------------------------------------------------------------')
